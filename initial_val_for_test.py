import restaurant_query_handeler
import delivery_query_handeler
import client_query_handler

# add five restaurant
b1 = restaurant_query_handeler.add_restaurant("A1", "12536985", "Meikhosh1", "2", "1111", "fast food", 20)
b2 = restaurant_query_handeler.add_restaurant("B2", "22536986", "Meikhosh2", "2", "2222", "traditional", 30)
b3 = restaurant_query_handeler.add_restaurant("C3", "32536987", "Meikhosh3", "3", "3333", "fast food", 40)
b4 = restaurant_query_handeler.add_restaurant("D4", "42536988", "Meikhosh4", "3", "4444", "traditional", 50)
b5 = restaurant_query_handeler.add_restaurant("E5", "52536989", "Meikhosh5", "4", "5555", "fast food", 60)
# add 3 food to each
restaurant_query_handeler.add_food_to_restaurant(b2, "Ash", "dessert", "in ye ghazaye alist", 10)
restaurant_query_handeler.add_food_to_restaurant(b2, "Kabab", "main", "in ye ghazaye alist", 12)
restaurant_query_handeler.add_food_to_restaurant(b2, "Sop", "pass ghaza", "in ye ghazaye alist", 9)

restaurant_query_handeler.add_food_to_restaurant(b1, "sibzamini", "dessert", "in ye ghazaye alist", 5)
restaurant_query_handeler.add_food_to_restaurant(b1, "hamberger", "main", "in ye ghazaye alist", 7)
restaurant_query_handeler.add_food_to_restaurant(b1, "jele", "pass ghaza", "in ye ghazaye alist", 3)

restaurant_query_handeler.add_food_to_restaurant(b3, "salad", "dessert", "in ye ghazaye alist", 6)
restaurant_query_handeler.add_food_to_restaurant(b3, "pizza", "main", "in ye ghazaye alist", 12)
restaurant_query_handeler.add_food_to_restaurant(b3, "sos", "pass ghaza", "in ye ghazaye alist", 3)

restaurant_query_handeler.add_food_to_restaurant(b4, "Torshi", "dessert", "in ye ghazaye alist", 1)
restaurant_query_handeler.add_food_to_restaurant(b4, "joje", "main", "in ye ghazaye alist", 122)
restaurant_query_handeler.add_food_to_restaurant(b4, "sabzi", "pass ghaza", "in ye ghazaye alist", 120)

restaurant_query_handeler.add_food_to_restaurant(b5, "berber", "dessert", "in ye ghazaye alist", 124)
restaurant_query_handeler.add_food_to_restaurant(b5, "pizpiz", "main", "in ye ghazaye alist", 126)
restaurant_query_handeler.add_food_to_restaurant(b5, "sosmos", "pass ghaza", "in ye ghazaye alist", 152)

# delivery
delivery_query_handeler.add_new_delivery("ali", 20, "2", "a", "a")
delivery_query_handeler.add_new_delivery("akbar", 20, "2", "b", "b")
delivery_query_handeler.add_new_delivery("sara", 40, "3", "c", "c")
delivery_query_handeler.add_new_delivery("mojan", 50, "3", "d", "d")
delivery_query_handeler.add_new_delivery("raha", 79, "4", "e", "e")
delivery_query_handeler.add_new_delivery("arshia", 90, "4", "f", "f")

# add test customer
c1 = client_query_handler.add_customer("test", "test", "arshia", "2", "9128381385")

# add discount
client_query_handler.add_discount_code(c1, 0.5, 20)
client_query_handler.add_discount_code(c1, 0.2, 10)
client_query_handler.add_discount_code(c1, 0.3, 70)
client_query_handler.add_discount_code(c1, 0.1, 40)

print("initial data added to the data base")
