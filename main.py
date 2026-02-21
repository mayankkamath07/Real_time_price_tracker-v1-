import time
from database import dbmanager  
from scrape import get_price   

def run_tracker():

    db = dbmanager()
    

    products = db.get_all_products()
    
    if not products:
        print("No products found in database. Add some first!")
        return

    print(f"Checking prices for {len(products)} items...")

    for p in products:
        p_id, p_name, p_url, target = p[0], p[1], p[2], p[3]
        
  
        current_price = get_price(p_url)
        
        if current_price:
          
            db.log_price(p_id, current_price)
            
            
            if current_price <= target:
                print(f"!!! ALERT: {p_name} is now ₹{current_price} (Target: ₹{target})")
            else:
                print(f"{p_name}: ₹{current_price} (Still above target)")
        else:
            print(f"Could not check price for {p_name}")
            
       
        time.sleep(2)

if __name__ == "__main__":
    run_tracker()