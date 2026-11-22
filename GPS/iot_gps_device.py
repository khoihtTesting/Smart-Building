import time

def get_region_name(lat, lon):
    # Nhận diện khu vực thông minh dựa trên tọa độ vùng TP.HCM và lân cận
    if 10.6 <= lat <= 11.0 and 106.5 <= lon <= 106.8:
        return "Ho Chi Minh City (Central Urban Area)"
    elif 10.2 <= lat <= 10.6 and 106.2 <= lon <= 106.5:
        return "Long An Province (Tan An Region)"
    elif 10.7 <= lat <= 11.1 and 106.7 <= lon <= 107.1:
        return "Dong Nai Province (Bien Hoa / Long Thanh Area)"
    elif 10.1 <= lat <= 10.5 and 107.0 <= lon <= 107.3:
        return "Ba Ria - Vung Tau Coastline"
    else:
        return "Southern Vietnam Region (VGU / Binh Duong / HCMC Sector)"

def run_virtual_iot_gps(filename):
    print("=" * 60)
    print("--- VIRTUAL IoT GPS DASHBOARD (LOCAL SMART RESOLVER) ---")
    print("=" * 60)
    
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            parts = line.split(",")
            sentence_type = parts[0]
            
            if sentence_type == "$GPGGA":
                time_utc = parts[1]
                raw_lat = parts[2]
                lat_dir = parts[3]
                raw_lon = parts[4]
                lon_dir = parts[5]
                altitude = f"{parts[9]} {parts[10]}"
                
                place_name = "Unknown Location"
                try:
                    if raw_lat and raw_lon:
                        # Chuẩn hóa định dạng NMEA sang Decimal Degrees
                        lat_split = raw_lat.split('.')
                        lat_deg = float(lat_split[0][:-2])
                        lat_min = float(lat_split[0][-2:] + '.' + lat_split[1])
                        lat_decimal = lat_deg + (lat_min / 60.0)
                        if lat_dir == 'S': lat_decimal = -lat_decimal
                        
                        lon_split = raw_lon.split('.')
                        lon_deg = float(lon_split[0][:-2])
                        lon_min = float(lon_split[0][-2:] + '.' + lon_split[1])
                        lon_decimal = lon_deg + (lon_min / 60.0)
                        if lon_dir == 'W': lon_decimal = -lon_decimal
                        
                        # Gọi hàm phân giải khu vực nội bộ
                        place_name = get_region_name(lat_decimal, lon_decimal)
                except Exception:
                    place_name = "Coordinate parsing error"

                formatted_time = f"{time_utc[:2]}:{time_utc[2:4]}:{time_utc[4:]}" if len(time_utc) >= 6 else time_utc
                print(f" [GPS FIX] Time (UTC): {formatted_time}")
                print(f" 📍 Location   : {place_name}")
                print(f" ⛰️ Altitude   : {altitude}")
                
            elif sentence_type == "$GPRMC":
                speed_knots = parts[7]
                date_str = parts[9]
                formatted_date = f"20{date_str[4:]}-{date_str[2:4]}-{date_str[:2]}" if len(date_str) == 6 else date_str
                
                try:
                    speed_kmh = float(speed_knots) * 1.852
                except:
                    speed_kmh = 0.0
                
                print(f" 📅 Date       : {formatted_date}")
                print(f" 🚀 Speed      : {speed_kmh:.2f} km/h ({speed_knots} knots)")
            
            print("-" * 60)
            time.sleep(1)
            
    except FileNotFoundError:
        print(f"❌ Error: File '{filename}' not found!")

if __name__ == "__main__":
    run_virtual_iot_gps("output.nmea")