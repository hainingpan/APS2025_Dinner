import yaml
import os

def calculate_bill():
    # Load the menu and people data
    with open('menu.yaml', 'r') as menu_file:
        menu = yaml.safe_load(menu_file)
    
    with open('people.yaml', 'r') as people_file:
        people = yaml.safe_load(people_file)
    
    # Calculate each person's subtotal
    totals = {}
    grand_subtotal = 0
    
    for person, orders in people.items():
        if not orders:  # People with no orders get $0
            totals[person] = 0
            continue
            
        person_subtotal = 0
        for order in orders:
            item = order['item']
            qty = order['quantity']
            price = menu.get(item, 0)
            person_subtotal += price * qty
            
        totals[person] = person_subtotal
        grand_subtotal += person_subtotal
    
    # Calculate tax and tip
    tax_rate = 0.0915  # Based on receipt
    tip_rate = 0.18
    
    tax = grand_subtotal * tax_rate
    tip = grand_subtotal * tip_rate
    grand_total = grand_subtotal + tax + tip
    actual_bill_total = 970.32  # From receipt
    
    # Print the payment breakdown first
    print("=" * 50)
    print(f"GRAND TOTAL: ${grand_subtotal:.2f}")
    print()
    print(f"Tax (9.15%): ${tax:.2f}")
    print(f"Tip (18%): ${tip:.2f}")
    print(f"TOTAL WITH TAX AND TIP: ${grand_total:.2f} out of ${actual_bill_total}")
    print()
    print("Payment breakdown:")
    
    # Show what each person owes (with proportion of tax and tip)
    for person, subtotal in totals.items():
        proportion = subtotal / grand_subtotal if grand_subtotal > 0 else 0
        person_tax = tax * proportion
        person_tip = tip * proportion
        person_total = subtotal + person_tax + person_tip
        
        response_status = "not yet response" if subtotal == 0 else ""
        print(f"{person}: ${person_total:.2f} {response_status}")
    
    print("=" * 50)
    print()
    
    # Print individual order details
    print("INDIVIDUAL ORDER DETAILS:")
    print("=" * 50)
    
    for person, orders in people.items():
        if not orders:  # Skip people with no orders in the details section
            continue
            
        print(f"\n{person}:")
        person_subtotal = 0
        
        for order in orders:
            item = order['item']
            qty = order['quantity']
            price = menu.get(item, 0)
            item_total = price * qty
            person_subtotal += item_total
            print(f"  {qty} x {item} (${price:.2f} each) = ${item_total:.2f}")
        
        proportion = person_subtotal / grand_subtotal if grand_subtotal > 0 else 0
        person_tax = tax * proportion
        person_tip = tip * proportion
        person_total = person_subtotal + person_tax + person_tip
        
        print(f"  Subtotal: ${person_subtotal:.2f}")
        print(f"  + Tax: ${person_tax:.2f}")
        print(f"  + Tip: ${person_tip:.2f}")
        print(f"  TOTAL: ${person_total:.2f}")

if __name__ == "__main__":
    calculate_bill()