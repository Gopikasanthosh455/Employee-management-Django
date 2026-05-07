def calculate_net_salary(gross_salary, is_contractor=False):
    """Section B Question 6: calculate salary after tax and optional contractor fee."""
    if gross_salary <= 3000:
        tax_rate = 0.10
    elif gross_salary <= 7000:
        tax_rate = 0.15
    else:
        tax_rate = 0.20

    net_salary = gross_salary - (gross_salary * tax_rate)

    if is_contractor:
        net_salary -= 100

    return net_salary
