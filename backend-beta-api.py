"""
UHY Beta Calculator - Backend API
Calcula beta através de regressão linear com dados históricos do Yahoo Finance
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from scipy import stats

app = Flask(__name__)
CORS(app)  # Permite requisições do frontend

# Mapeamento de índices de mercado
MARKET_INDICES = {
    'US': '^GSPC',      # S&P 500
    'BR': '^BVSP',      # IBOVESPA
    'UK': '^FTSE',      # FTSE 100
    'JP': '^N225',      # Nikkei 225
    'DE': '^GDAXI',     # DAX
    'FR': '^FCHI',      # CAC 40
    'CA': '^GSPTSE',    # TSX
    'AU': '^AXJO',      # ASX 200
}

def determinar_indice(ticker):
    """Determina o índice de mercado baseado no ticker"""
    ticker = ticker.upper()
    
    if ticker.endswith('.SA'):
        return '^BVSP', 'IBOVESPA'
    elif ticker.endswith('.L'):
        return '^FTSE', 'FTSE 100'
    elif ticker.endswith('.T'):
        return '^N225', 'Nikkei 225'
    elif ticker.endswith('.DE'):
        return '^GDAXI', 'DAX'
    elif ticker.endswith('.PA'):
        return '^FCHI', 'CAC 40'
    elif ticker.endswith('.TO'):
        return '^GSPTSE', 'TSX'
    elif ticker.endswith('.AX'):
        return '^AXJO', 'ASX 200'
    else:
        return '^GSPC', 'S&P 500'

def calcular_beta(ticker, periodo_anos=2, frequencia='weekly', data_base=None):
    """
    Calcula beta através de regressão linear
    
    Args:
        ticker: código da ação
        periodo_anos: 1, 2, ou 5 anos
        frequencia: 'daily', 'weekly', ou 'monthly'
        data_base: data final (default: hoje)
    
    Returns:
        dict com beta, índice usado, R², etc
    """
    try:
        # Data base
        if data_base:
            end_date = pd.to_datetime(data_base)
        else:
            end_date = datetime.now()
        
        start_date = end_date - timedelta(days=periodo_anos * 365)
        
        # Determinar índice de mercado
        indice_ticker, indice_nome = determinar_indice(ticker)
        
        # Baixar dados históricos
        stock = yf.download(ticker, start=start_date, end=end_date, progress=False)
        market = yf.download(indice_ticker, start=start_date, end=end_date, progress=False)
        
        if stock.empty or market.empty:
            return {
                'sucesso': False,
                'erro': f'Não foi possível baixar dados para {ticker}'
            }
        
        # Usar preço ajustado
        stock_prices = stock['Adj Close']
        market_prices = market['Adj Close']
        
        # Reamostrar conforme frequência
        if frequencia == 'weekly':
            stock_prices = stock_prices.resample('W').last()
            market_prices = market_prices.resample('W').last()
        elif frequencia == 'monthly':
            stock_prices = stock_prices.resample('M').last()
            market_prices = market_prices.resample('M').last()
        # daily não precisa reamostrar
        
        # Calcular retornos
        stock_returns = stock_prices.pct_change().dropna()
        market_returns = market_prices.pct_change().dropna()
        
        # Alinhar datas (interseção)
        aligned_data = pd.DataFrame({
            'stock': stock_returns,
            'market': market_returns
        }).dropna()
        
        if len(aligned_data) < 20:
            return {
                'sucesso': False,
                'erro': f'Dados insuficientes: apenas {len(aligned_data)} observações'
            }
        
        # Regressão linear: R_stock = alpha + beta * R_market
        slope, intercept, r_value, p_value, std_err = stats.linregress(
            aligned_data['market'],
            aligned_data['stock']
        )
        
        # Beta é o slope (coeficiente angular)
        beta = slope
        r_squared = r_value ** 2
        
        # Informações adicionais
        correlacao = aligned_data['stock'].corr(aligned_data['market'])
        volatilidade_stock = aligned_data['stock'].std() * np.sqrt(252 if frequencia == 'daily' else (52 if frequencia == 'weekly' else 12))
        volatilidade_market = aligned_data['market'].std() * np.sqrt(252 if frequencia == 'daily' else (52 if frequencia == 'weekly' else 12))
        
        return {
            'sucesso': True,
            'ticker': ticker,
            'beta': round(beta, 4),
            'r_squared': round(r_squared, 4),
            'alpha': round(intercept, 6),
            'p_value': round(p_value, 6),
            'std_err': round(std_err, 4),
            'correlacao': round(correlacao, 4),
            'volatilidade_stock': round(volatilidade_stock, 4),
            'volatilidade_market': round(volatilidade_market, 4),
            'indice': indice_nome,
            'indice_ticker': indice_ticker,
            'num_observacoes': len(aligned_data),
            'periodo_anos': periodo_anos,
            'frequencia': frequencia,
            'data_inicio': aligned_data.index[0].strftime('%Y-%m-%d'),
            'data_fim': aligned_data.index[-1].strftime('%Y-%m-%d'),
            'metodologia': f'Regressão linear com {len(aligned_data)} observações ({frequencia}) de {aligned_data.index[0].strftime("%Y-%m-%d")} a {aligned_data.index[-1].strftime("%Y-%m-%d")} vs {indice_nome}'
        }
        
    except Exception as e:
        return {
            'sucesso': False,
            'erro': str(e)
        }

def obter_dados_financeiros(ticker):
    """
    Obtém dados financeiros via yfinance
    """
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        
        # Market Cap
        market_cap = info.get('marketCap', 0)
        if market_cap > 1e9:
            market_cap_fmt = f"${market_cap/1e9:.2f}B"
        elif market_cap > 1e6:
            market_cap_fmt = f"${market_cap/1e6:.2f}M"
        else:
            market_cap_fmt = "N/D"
        
        # Dívida e Caixa
        total_debt = info.get('totalDebt', 0)
        cash = info.get('totalCash', 0)
        net_debt = total_debt - cash
        
        if net_debt > 1e9:
            net_debt_fmt = f"${net_debt/1e9:.2f}B"
        elif net_debt > 1e6:
            net_debt_fmt = f"${net_debt/1e6:.2f}M"
        else:
            net_debt_fmt = "$0"
        
        # D/E
        if market_cap > 0:
            de_ratio = net_debt / market_cap
        else:
            de_ratio = 0
        
        # Enterprise Value
        ev = info.get('enterpriseValue', 0)
        if ev > 1e9:
            ev_fmt = f"${ev/1e9:.2f}B"
        elif ev > 1e6:
            ev_fmt = f"${ev/1e6:.2f}M"
        else:
            ev_fmt = "N/D"
        
        # EBITDA
        ebitda = info.get('ebitda', 0)
        if ebitda > 1e9:
            ebitda_fmt = f"${ebitda/1e9:.2f}B"
        elif ebitda > 1e6:
            ebitda_fmt = f"${ebitda/1e6:.2f}M"
        else:
            ebitda_fmt = "N/D"
        
        # EV/EBITDA
        if ebitda > 0 and ev > 0:
            ev_ebitda = ev / ebitda
        else:
            ev_ebitda = None
        
        # Determinar país e taxa de imposto
        country = info.get('country', 'US')
        if country == 'Brazil' or ticker.endswith('.SA'):
            tax_rate = '34%'
        elif country in ['United States', 'Canada']:
            tax_rate = '21%'
        else:
            tax_rate = '25%'
        
        return {
            'nome': info.get('longName', ticker),
            'setor': info.get('sector', 'N/D'),
            'industria': info.get('industry', 'N/D'),
            'marketCap': market_cap_fmt,
            'marketCapNumerico': market_cap,
            'dividaLiquida': net_debt_fmt,
            'deRatio': round(de_ratio, 4),
            'enterpriseValue': ev_fmt,
            'ebitda': ebitda_fmt,
            'evEbitda': round(ev_ebitda, 2) if ev_ebitda else None,
            'taxaImposto': tax_rate,
            'pais': country
        }
        
    except Exception as e:
        return {
            'erro': str(e)
        }

@app.route('/calcular-beta', methods=['POST'])
def calcular_beta_endpoint():
    """
    Endpoint principal para cálculo de beta
    
    POST /calcular-beta
    Body: {
        "ticker": "AAPL",
        "periodo": 2,
        "frequencia": "weekly",
        "data_base": "2024-12-31"  // opcional
    }
    """
    data = request.json
    
    ticker = data.get('ticker')
    periodo = data.get('periodo', 2)
    frequencia = data.get('frequencia', 'weekly')
    data_base = data.get('data_base')
    
    if not ticker:
        return jsonify({'erro': 'Ticker não fornecido'}), 400
    
    # Calcular beta
    resultado_beta = calcular_beta(ticker, periodo, frequencia, data_base)
    
    if not resultado_beta.get('sucesso'):
        return jsonify(resultado_beta), 400
    
    # Obter dados financeiros
    dados_financeiros = obter_dados_financeiros(ticker)
    
    # Calcular beta desalavancado
    beta_alav = resultado_beta['beta']
    de_ratio = dados_financeiros.get('deRatio', 0)
    tax_rate_str = dados_financeiros.get('taxaImposto', '21%')
    tax_rate = float(tax_rate_str.strip('%')) / 100
    
    if de_ratio > 0:
        beta_desalav = beta_alav / (1 + (1 - tax_rate) * de_ratio)
    else:
        beta_desalav = beta_alav
    
    # Combinar resultados
    resultado_completo = {
        **resultado_beta,
        **dados_financeiros,
        'betaAlavancado': round(beta_alav, 4),
        'betaDesalavancado': round(beta_desalav, 4)
    }
    
    return jsonify(resultado_completo)

@app.route('/calcular-multiplos', methods=['POST'])
def calcular_multiplos_endpoint():
    """
    Endpoint para calcular betas de múltiplos tickers
    
    POST /calcular-multiplos
    Body: {
        "tickers": ["AAPL", "MSFT", "GOOGL"],
        "periodo": 2,
        "frequencia": "weekly",
        "data_base": "2024-12-31"
    }
    """
    data = request.json
    
    tickers = data.get('tickers', [])
    periodo = data.get('periodo', 2)
    frequencia = data.get('frequencia', 'weekly')
    data_base = data.get('data_base')
    
    if not tickers:
        return jsonify({'erro': 'Nenhum ticker fornecido'}), 400
    
    resultados = []
    
    for ticker in tickers:
        resultado_beta = calcular_beta(ticker, periodo, frequencia, data_base)
        
        if resultado_beta.get('sucesso'):
            dados_financeiros = obter_dados_financeiros(ticker)
            
            beta_alav = resultado_beta['beta']
            de_ratio = dados_financeiros.get('deRatio', 0)
            tax_rate_str = dados_financeiros.get('taxaImposto', '21%')
            tax_rate = float(tax_rate_str.strip('%')) / 100
            
            if de_ratio > 0:
                beta_desalav = beta_alav / (1 + (1 - tax_rate) * de_ratio)
            else:
                beta_desalav = beta_alav
            
            resultado_completo = {
                **resultado_beta,
                **dados_financeiros,
                'betaAlavancado': round(beta_alav, 4),
                'betaDesalavancado': round(beta_desalav, 4)
            }
            
            resultados.append(resultado_completo)
        else:
            resultados.append({
                'ticker': ticker,
                'sucesso': False,
                'erro': resultado_beta.get('erro')
            })
    
    return jsonify({'resultados': resultados})

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'ok', 'message': 'UHY Beta Calculator API funcionando'})

if __name__ == '__main__':
    import os
    
    port = int(os.environ.get('PORT', 5000))
    
    print("🚀 UHY Beta Calculator API")
    print("📊 Calculando betas via regressão linear com Yahoo Finance")
    print(f"🌐 Servidor rodando na porta {port}")
    print("\nEndpoints disponíveis:")
    print("  POST /calcular-beta - Calcula beta para um ticker")
    print("  POST /calcular-multiplos - Calcula beta para múltiplos tickers")
    print("  GET  /health - Health check")
    
    app.run(debug=False, host='0.0.0.0', port=port)
