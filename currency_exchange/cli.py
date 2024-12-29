import click
import pandas as pd
from datetime import datetime
from typing import Optional
from .api.client import ForexAPIClient
from .services.exchange_service import ExchangeService
from .utils.validators import validate_currency_code, validate_date

@click.group()
def cli():
    """Currency Exchange Rate CLI"""
    pass

@cli.command()
@click.option('--amount', type=float, required=True, help='Amount to convert')
@click.option('--from', 'from_currency', required=True, help='Source currency code')
@click.option('--to', 'to_currency', required=True, help='Target currency code')
def convert(amount: float, from_currency: str, to_currency: str):
    """Convert amount between currencies"""
    try:
        validate_currency_code(from_currency)
        validate_currency_code(to_currency)
        
        client = ForexAPIClient()
        service = ExchangeService(client)
        
        result = service.convert_currency(amount, from_currency, to_currency)
        click.echo(f"{amount} {from_currency} = {result:.2f} {to_currency}")
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)

@cli.command()
@click.option('--base', default='EUR', help='Base currency code')
@click.option('--symbols', help='Comma-separated target currency codes')
def latest(base: str, symbols: Optional[str]):
    """Get latest exchange rates"""
    try:
        validate_currency_code(base)
        symbol_list = symbols.split(',') if symbols else None
        if symbol_list:
            for symbol in symbol_list:
                validate_currency_code(symbol)
        
        client = ForexAPIClient()
        rates = client.get_latest_rates(base=base, symbols=symbol_list)
        
        df = pd.DataFrame([rates['rates']]).T
        df.columns = ['Rate']
        click.echo(f"\nExchange rates for {base} on {rates['date']}:\n")
        click.echo(df.to_string())
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)

@cli.command()
@click.option('--base', default='EUR', help='Base currency code')
@click.option('--symbols', help='Comma-separated target currency codes')
@click.option('--days', default=30, help='Number of days for trend analysis')
def trends(base: str, symbols: str, days: int):
    """Analyze currency rate trends"""
    try:
        validate_currency_code(base)
        symbol_list = symbols.split(',')
        for symbol in symbol_list:
            validate_currency_code(symbol)
        
        client = ForexAPIClient()
        service = ExchangeService(client)
        
        df = service.get_rate_trends(base, symbol_list, days)
        
        click.echo(f"\nTrend analysis for {base} over {days} days:\n")
        for currency in symbol_list:
            stats = df[currency].describe()
            click.echo(f"\n{currency}:")
            click.echo(f"  Average rate: {stats['mean']:.4f}")
            click.echo(f"  Min rate: {stats['min']:.4f}")
            click.echo(f"  Max rate: {stats['max']:.4f}")
            click.echo(f"  Volatility: {stats['std']:.4f}")
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)

if __name__ == '__main__':
    cli()
