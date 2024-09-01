import requests
import os
import sys
import time
from datetime import datetime

def check_url_status(url):
    try:
        response = requests.get(url, timeout=10)  # Set a timeout for the request
        return str(response.status_code)  # Ensure status_code is a string
    except requests.RequestException:
        return 'Unreachable'  # Print a  message

def display_progress(current, total):
    progress = int((current / total) * 100)
    sys.stdout.write(f'\rProgress: [{progress * "="}{(100 - progress) * " "}] {progress}% ({current}/{total})')
    sys.stdout.flush()

def generate_html_report(up_urls, down_urls):
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Website Status Report</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; }}
            table {{ width: 100%; border-collapse: collapse; }}
            th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
            th {{ background-color: #f4f4f4; }}
            .up {{ background-color: #d4edda; color: #155724; }}
            .down {{ background-color: #f8d7da; color: #721c24; }}
            .error {{ background-color: #f8d7da; color: #721c24; }}
            h2 {{ color: #333; }}
        </style>
    </head>
    <body>
        <h1>Website Status Report</h1>
        <h2>Summary</h2>
        <p>Total URLs: {len(up_urls) + len(down_urls)}</p>
        <p>Reachable URLs: {len(up_urls)}</p>
        <p>Unreachable URLs: {len(down_urls)}</p>
        <h2>Reachable URLs</h2>
        <table>
            <thead>
                <tr>
                    <th>URL</th>
                    <th>Status Code</th>
                </tr>
            </thead>
            <tbody>
    """
    for url, status in up_urls:
        html_content += f"""
                <tr class="up">
                    <td>{url}</td>
                    <td>{status}</td>
                </tr>
        """

    html_content += """
            </tbody>
        </table>
        <h2>Unreachable URLs</h2>
        <table>
            <thead>
                <tr>
                    <th>URL</th>
                    <th>Status Code</th>
                </tr>
            </thead>
            <tbody>
    """

    for url, status in down_urls:
        html_content += f"""
                <tr class="down">
                    <td>{url}</td>
                    <td>{status}</td>
                </tr>
        """

    html_content += """
            </tbody>
        </table>
    </body>
    </html>
    """

    with open('website_status_report.html', 'w') as file:
        file.write(html_content)

def main():
    input_file = 'A2.txt'
    up_urls = []
    down_urls = []

    if not os.path.exists(input_file):
        print(f"The file {input_file} does not exist.")
        return

    with open(input_file, 'r') as file:
        urls = [line.strip().split(',')[0] for line in file]
    
    total_urls = len(urls)
    print(f"\nDate and Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Total URLs to check: {total_urls}")

    for i, url in enumerate(urls):
        status_code = check_url_status(url)
        if status_code.startswith('2'):
            up_urls.append((url, status_code))
        else:
            down_urls.append((url, status_code))
        
        # Update progress bar
        display_progress(i + 1, total_urls)
        time.sleep(0.1)  # Optional: add a small delay to simulate progress (remove if not needed)

    # Print a new line to end the progress bar line
    print("\n")

    generate_html_report(up_urls, down_urls)
    print("HTML file created: website_status_report.html")

if __name__ == '__main__':
    main()
