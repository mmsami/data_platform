# src/utils/dashboard.py
import os
from datetime import datetime
from typing import Dict
from src.utils.logger import logger

class Dashboard:
    @staticmethod
    def generate_html(status_data: Dict) -> str:
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Define CSS separately
        css = """
            body { 
                font-family: sans-serif; 
                margin: 20px; 
            }
            .task-card { 
                border: 1px solid #ddd;
                border-radius: 8px;
                padding: 15px;
                margin: 10px 0;
                background-color: #f8f9fa;
            }
            .success { color: green; }
            .error { color: red; }
            .running { color: blue; }
            .metric { 
                display: inline-block;
                margin-right: 20px;
            }
        """

        # Start HTML
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Data Platform Status</title>
            <meta http-equiv="refresh" content="60">
            <style>
                {css}
            </style>
        </head>
        <body>
            <h1>Data Platform Status</h1>
            <p>Last Updated: {current_time}</p>
        """

        # Add task cards
        for task_name, status in status_data.items():
            success_rate = status['success_rate'] * 100
            status_class = 'running' if status['is_running'] else 'success'
            if status['last_error']:
                status_class = 'error'

            last_run = status['last_run'].strftime('%Y-%m-%d %H:%M:%S') if status['last_run'] else 'Never'
            last_success = status['last_success'].strftime('%Y-%m-%d %H:%M:%S') if status['last_success'] else 'Never'

            html += f"""
            <div class="task-card">
                <h2>{task_name}</h2>
                <div class="metric">
                    <strong>Status: </strong>
                    <span class="{status_class}">
                        {'Running' if status['is_running'] else 'Idle'}
                    </span>
                </div>
                <div class="metric">
                    <strong>Success Rate: </strong>
                    {success_rate:.1f}%
                </div>
                <div class="metric">
                    <strong>Total Runs: </strong>
                    {status['total_runs']}
                </div>
                <br>
                <div class="metric">
                    <strong>Last Run: </strong>
                    {last_run}
                </div>
                <div class="metric">
                    <strong>Last Success: </strong>
                    {last_success}
                </div>
            """
            
            if status['last_error']:
                html += f"""
                <div class="error">
                    <strong>Last Error: </strong>
                    {status['last_error']}
                </div>
                """
            html += "</div>"

        # Close HTML
        html += """
        </body>
        </html>
        """
        
        return html

    @staticmethod
    def save_dashboard(status_data: Dict, dashboard_dir: str = "dashboards") -> str:
        try:
            # Create directory if it doesn't exist
            os.makedirs(dashboard_dir, exist_ok=True)
            
            # Full path for dashboard
            dashboard_path = os.path.join(os.getcwd(), dashboard_dir, "dashboard.html")
            
            # Generate and save HTML
            html_content = Dashboard.generate_html(status_data)
            with open(dashboard_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            logger.info(f"Dashboard saved to: {dashboard_path}")
            return dashboard_path
            
        except Exception as e:
            logger.error(f"Error saving dashboard: {str(e)}")
            raise