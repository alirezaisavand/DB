import restaurant_query_handeler
import delivery_query_handeler
import client_query_handler

# add five restaurant
b1 = restaurant_query_handeler.add_new_restaurant("A1", "12536985", "2", "fast food", 20)
b2 = restaurant_query_handeler.add_new_restaurant("B2", "22536986", "2", "traditional", 30)
b3 = restaurant_query_handeler.add_new_restaurant("C3", "32536987", "3", "fast food", 40)
b4 = restaurant_query_handeler.add_new_restaurant("D4", "42536988", "3", "traditional", 50)
b5 = restaurant_query_handeler.add_new_restaurant("E5", "52536989", "4", "fast food", 60)
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
delivery_query_handeler.add_new_delivery("ali", 20, "2")
delivery_query_handeler.add_new_delivery("akbar", 20, "2")
delivery_query_handeler.add_new_delivery("sara", 40, "3")
delivery_query_handeler.add_new_delivery("mojan", 50, "3")
delivery_query_handeler.add_new_delivery("raha", 79, "4")
delivery_query_handeler.add_new_delivery("arshia", 90, "4")

print("initial data added to the data base")