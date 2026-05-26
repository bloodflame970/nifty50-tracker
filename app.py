import os
import io
from flask import Flask, render_template, jsonify, request, Response, make_response
import pandas as pd
from database import get_nifty_data, get_summary_metrics, update_nifty_data

app = Flask(__name__)

# Ensure templates and static are relative to this app file
app.template_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app.static_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')

@app.route('/')
def index():
    """Render the dashboard page."""
    return render_template('index.html')

@app.route('/api/summary')
def api_summary():
    """Endpoint returning Nifty 50 performance summary metrics."""
    try:
        metrics = get_summary_metrics()
        return jsonify({
            'success': True,
            'metrics': metrics
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/data')
def api_data():
    """Endpoint returning Nifty 50 data as JSON for charting."""
    interval = request.args.get('interval', 'daily')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    limit = request.args.get('limit', type=int)
    
    if interval not in ['daily', 'weekly', 'monthly']:
        return jsonify({'success': False, 'error': 'Invalid interval'}), 400
        
    try:
        df = get_nifty_data(interval=interval, start_date=start_date, end_date=end_date, limit=limit)
        # Convert df to dictionary format for JSON response
        data_list = df.to_dict('records')
        return jsonify({
            'success': True,
            'interval': interval,
            'count': len(data_list),
            'data': data_list
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/update', methods=['POST'])
def api_update():
    """Endpoint to trigger an update of the local Nifty database from yfinance."""
    try:
        status = update_nifty_data()
        all_success = all(status.values())
        return jsonify({
            'success': all_success,
            'status': status
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/download')
def api_download():
    """Endpoint to download Nifty 50 data as CSV or JSON."""
    interval = request.args.get('interval', 'daily')
    file_format = request.args.get('format', 'csv').lower()
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    if interval not in ['daily', 'weekly', 'monthly']:
        return "Invalid interval", 400
        
    if file_format not in ['csv', 'json']:
        return "Invalid format", 400
        
    try:
        df = get_nifty_data(interval=interval, start_date=start_date, end_date=end_date)
        
        # Format filename
        date_str = pd.Timestamp.now().strftime('%Y%m%d')
        filename = f"nifty50_{interval}_{date_str}.{file_format}"
        
        if file_format == 'csv':
            # Create a CSV response
            output = io.StringIO()
            df.to_csv(output, index=False)
            csv_data = output.getvalue()
            
            return Response(
                csv_data,
                mimetype="text/csv",
                headers={"Content-disposition": f"attachment; filename={filename}"}
            )
        else:
            # Create a JSON response
            json_data = df.to_json(orient='records', indent=2)
            
            return Response(
                json_data,
                mimetype="application/json",
                headers={"Content-disposition": f"attachment; filename={filename}"}
            )
            
    except Exception as e:
        return f"Error generating download: {str(e)}", 500

if __name__ == '__main__':
    # Initialize the database and populate if empty
    try:
        df = get_nifty_data(limit=1)
        if df.empty:
            print("Database is empty. Populating with initial Nifty 50 data...")
            update_nifty_data()
    except Exception as e:
        print(f"Error checking/initializing database on startup: {e}")
        update_nifty_data()
        
    app.run(debug=True, host='0.0.0.0', port=5000)
