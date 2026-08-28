from flask import Flask, request, Response
import requests
import json

app = Flask(__name__)

def fetch_data_from_source(query_number):
    try:
        api_url = f"https://osint.invalidayushh.workers.dev/num?key=69d&q={query_number}"
        response = requests.get(api_url, timeout=30)
        
        if response.status_code == 200:
            return response.json()
        else:
            return {}
            
    except Exception as e:
        print(f"Error: {e}")
        return {}

@app.route('/api/lookup', methods=['GET'])
def mobile_lookup():
    query_number = request.args.get('query')
    
    if not query_number:
        error_json = {"❌_Error": "Please provide a query number. Example: ?query=1234567890"}
        json_output = json.dumps(error_json, ensure_ascii=False, indent=4)
        return Response(json_output, status=400, content_type='application/json; charset=utf-8')

    raw_response = fetch_data_from_source(query_number)
    raw_data = raw_response.get("data", {})
    
    # SCENARIO 1: AGAR RESULT EMPTY HAI YA API FAIL HO JAYE
    if not raw_data or raw_response.get("Success") is False:
        custom_empty_json = {
            "🔍_Status": "Not Found",
            "📌_Query": query_number,
            "⚠️_Message": "No records found for this number.",
            "💌_BUY_PREMIUM_API_FROM": {
                "🔥_Message": "Buy Premium API with Full Database Here",
                "👑_Developer": "@Aditya_dark0",
                "🛠️_Support": "@Aditya_Elite",
                "📢_Channel": "https://t.me/AdityaXosint"
            }
        }
        json_output = json.dumps(custom_empty_json, ensure_ascii=False, indent=4)
        return Response(json_output, status=200, content_type='application/json; charset=utf-8')
    
    # SCENARIO 2: AGAR DATA MIL JATA HAI
    else:
        filtered_results = []
        
        keys_to_remove = ["key_details", "success", "status_code", "http_status"]
        for k in keys_to_remove:
            raw_data.pop(k, None)
            
        count = 0
        for key, res in raw_data.items():
            if not isinstance(res, dict):
                continue
                
            count += 1
            raw_address = res.get("ADDRESS", "")
            clean_address = raw_address.replace("!", ", ") if raw_address and raw_address != "0" else "N/A"
            
            result_obj = {
                "🪪_Aadhaar": res.get("aadhar", "N/A"), 
                "👤_Name": res.get("NAME", "N/A"),
                "👨‍👦_Father": res.get("fname", "N/A"),
                "📱_Mobile": res.get("num", "N/A")
            }
            
            if res.get("alt"):
                result_obj["📞_Alternate"] = res.get("alt")
                
            if clean_address != "N/A":
                result_obj["🏠_Address"] = clean_address
                
            if res.get("circle"):
                result_obj["📡_Circle"] = res.get("circle")
                
            filtered_results.append({f"📋_Result_{count}": result_obj})

        success_json = {
            "🔍_Title": "📱 MOBILE LOOKUP RESULT",
            "📌_Number": query_number,
            "📊_Results_Found": count,
            "📋_Data": filtered_results,
            "💌_BUY_PREMIUM_API_FROM": {
                "👑_Developer": "@Aditya_dark0",
                "🛠️_Support": "@Aditya_Elite",
                "📢_Channel": "https://t.me/AdityaXosint"
            }
        }
        
        json_output = json.dumps(success_json, ensure_ascii=False, indent=4)
        return Response(json_output, status=200, content_type='application/json; charset=utf-8')

if __name__ == '__main__':
    # Port change karke 8080 set kiya gaya hai taaki clash na ho
    app.run(host='0.0.0.0', port=8080)