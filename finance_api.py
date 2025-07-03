import yfinance as yf
import pandas as pd
import json
from datetime import datetime, timedelta
import requests

class FinanceAPI:
    def __init__(self):
        """Inicializa a classe de API financeira"""
        self.popular_stocks = {
            # Ações Brasileiras
            'PETR4.SA': 'Petrobras',
            'VALE3.SA': 'Vale',
            'ITUB4.SA': 'Itaú Unibanco',
            'BBDC4.SA': 'Bradesco',
            'ABEV3.SA': 'Ambev',
            'MGLU3.SA': 'Magazine Luiza',
            'WEGE3.SA': 'WEG',
            'SUZB3.SA': 'Suzano',
            'RENT3.SA': 'Localiza',
            'LREN3.SA': 'Lojas Renner',
            
            # Ações Americanas
            'AAPL': 'Apple',
            'MSFT': 'Microsoft',
            'GOOGL': 'Google/Alphabet',
            'AMZN': 'Amazon',
            'TSLA': 'Tesla',
            'META': 'Meta (Facebook)',
            'NVDA': 'NVIDIA',
            'NFLX': 'Netflix',
            'DIS': 'Disney',
            'COCA': 'Coca-Cola',
            
            # Criptomoedas
            'BTC-USD': 'Bitcoin',
            'ETH-USD': 'Ethereum',
            'ADA-USD': 'Cardano',
            'SOL-USD': 'Solana',
            
            # Índices
            '^BVSP': 'Ibovespa',
            '^GSPC': 'S&P 500',
            '^DJI': 'Dow Jones',
            '^IXIC': 'NASDAQ'
        }
    
    def get_stock_info(self, symbol):
        """Obtém informações básicas de uma ação"""
        try:
            stock = yf.Ticker(symbol.upper())
            info = stock.info
            
            # Dados básicos
            current_price = info.get('currentPrice', info.get('regularMarketPrice', 'N/A'))
            previous_close = info.get('previousClose', 'N/A')
            company_name = info.get('longName', info.get('shortName', symbol))
            
            # Calcula variação
            if current_price != 'N/A' and previous_close != 'N/A':
                change = current_price - previous_close
                change_percent = (change / previous_close) * 100
            else:
                change = change_percent = 'N/A'
            
            return {
                'symbol': symbol.upper(),
                'name': company_name,
                'current_price': current_price,
                'previous_close': previous_close,
                'change': change,
                'change_percent': change_percent,
                'currency': info.get('currency', 'USD'),
                'market_cap': info.get('marketCap', 'N/A'),
                'volume': info.get('volume', 'N/A'),
                'pe_ratio': info.get('trailingPE', 'N/A'),
                'dividend_yield': info.get('dividendYield', 'N/A'),
                'day_high': info.get('dayHigh', 'N/A'),
                'day_low': info.get('dayLow', 'N/A'),
                'week_52_high': info.get('fiftyTwoWeekHigh', 'N/A'),
                'week_52_low': info.get('fiftyTwoWeekLow', 'N/A')
            }
        except Exception as e:
            return {'error': f'Erro ao buscar dados para {symbol}: {str(e)}'}
    
    def get_stock_history(self, symbol, period='1mo'):
        """Obtém histórico de preços"""
        try:
            stock = yf.Ticker(symbol.upper())
            hist = stock.history(period=period)
            
            if hist.empty:
                return {'error': f'Nenhum dado encontrado para {symbol}'}
            
            # Últimos 5 dias
            recent_data = hist.tail(5)
            history_data = []
            
            for date, row in recent_data.iterrows():
                history_data.append({
                    'date': date.strftime('%Y-%m-%d'),
                    'open': round(row['Open'], 2),
                    'high': round(row['High'], 2),
                    'low': round(row['Low'], 2),
                    'close': round(row['Close'], 2),
                    'volume': int(row['Volume'])
                })
            
            return {
                'symbol': symbol.upper(),
                'period': period,
                'data': history_data
            }
        except Exception as e:
            return {'error': f'Erro ao buscar histórico para {symbol}: {str(e)}'}
    
    def search_stocks(self, query):
        """Busca ações por nome ou símbolo"""
        results = []
        query_lower = query.lower()
        
        # Busca nas ações populares
        for symbol, name in self.popular_stocks.items():
            if (query_lower in symbol.lower() or 
                query_lower in name.lower()):
                results.append({
                    'symbol': symbol,
                    'name': name,
                    'type': self._get_asset_type(symbol)
                })
        
        return results[:10]  # Limita a 10 resultados
    
    def _get_asset_type(self, symbol):
        """Determina o tipo do ativo"""
        if symbol.endswith('.SA'):
            return 'Ação Brasileira'
        elif symbol.endswith('-USD'):
            return 'Criptomoeda'
        elif symbol.startswith('^'):
            return 'Índice'
        else:
            return 'Ação Internacional'
    
    def get_market_summary(self):
        """Obtém resumo dos principais índices"""
        indices = ['^BVSP', '^GSPC', '^DJI', '^IXIC']
        summary = []
        
        for index in indices:
            try:
                data = self.get_stock_info(index)
                if 'error' not in data:
                    summary.append({
                        'name': data['name'],
                        'symbol': data['symbol'],
                        'price': data['current_price'],
                        'change': data['change'],
                        'change_percent': data['change_percent']
                    })
            except:
                continue
        
        return summary
    
    def get_trending_stocks(self):
        """Obtém ações em alta (simulado com ações populares)"""
        trending = ['PETR4.SA', 'VALE3.SA', 'AAPL', 'TSLA', 'BTC-USD']
        results = []
        
        for symbol in trending:
            try:
                data = self.get_stock_info(symbol)
                if 'error' not in data:
                    results.append({
                        'symbol': data['symbol'],
                        'name': data['name'],
                        'price': data['current_price'],
                        'change_percent': data['change_percent']
                    })
            except:
                continue
        
        return results
    
    def format_currency(self, value, currency='BRL'):
        """Formata valores monetários"""
        if value == 'N/A' or value is None:
            return 'N/A'
        
        try:
            if currency == 'BRL':
                return f'R$ {value:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.')
            else:
                return f'${value:,.2f}'
        except:
            return str(value)
    
    def format_large_number(self, value):
        """Formata números grandes (milhões, bilhões)"""
        if value == 'N/A' or value is None:
            return 'N/A'
        
        try:
            if value >= 1e12:
                return f'{value/1e12:.2f}T'
            elif value >= 1e9:
                return f'{value/1e9:.2f}B'
            elif value >= 1e6:
                return f'{value/1e6:.2f}M'
            elif value >= 1e3:
                return f'{value/1e3:.2f}K'
            else:
                return f'{value:,.0f}'
        except:
            return str(value)
