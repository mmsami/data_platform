# src/reports/templates.py
from datetime import datetime
from typing import Dict

class ReportTemplate:
    @staticmethod
    def daily_report_template(data: Dict) -> str:
        return f"""
        <html>
        <body>
        <h1>Daily Market Report - {datetime.now().strftime('%Y-%m-%d')}</h1>
        
        <h2>Price Summary</h2>
        <p>High: {data['price_summary']['high']}</p>
        <p>Low: {data['price_summary']['low']}</p>
        <p>Average: {data['price_summary']['average']}</p>
        
        <h2>Significant Moves</h2>
        {''.join(f"<p>{move['timestamp']}: {move['price_change']}% change</p>" 
                 for move in data['significant_moves'])}
        
        <h2>News Summary</h2>
        <p>Total news items: {data['news_summary']['count']}</p>
        {''.join(f"<p>- {news['title']}</p>" 
                 for news in data['news_summary']['latest'])}
        
        <h2>Alerts</h2>
        {''.join(f"<p>{alert}</p>" for alert in data['alerts'])}
        </body>
        </html>
        """

    @staticmethod
    def weekly_report_template(data: Dict) -> str:
        return f"""
        <html>
        <body>
        <h1>Weekly Market Report - Week of {datetime.now().strftime('%Y-%m-%d')}</h1>
        
        <h2>Weekly Summary</h2>
        <p>Starting Price: {data['price_summary']['start_price']}</p>
        <p>Ending Price: {data['price_summary']['end_price']}</p>
        <p>Weekly Change: {data['price_summary']['change_percentage']:.1f}%</p>
        <p>Weekly Range: {data['price_summary']['low']} - {data['price_summary']['high']}</p>
        
        <h2>Major Moves This Week</h2>
        {''.join(f"<p>{move['timestamp']}: {move['price_change']}% change</p>" 
                 for move in data['significant_moves'])}
        
        <h2>Top Headlines</h2>
        {''.join(f"<p>- {headline}</p>" 
                 for headline in data['news_summary']['major_headlines'])}
        
        <h2>Weekly Alerts</h2>
        {''.join(f"<p>{alert}</p>" for alert in data['alerts'])}
        </body>
        </html>
        """