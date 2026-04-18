from utils.db import get_db_connection
class ProductModel:
    @staticmethod
    def get_all_products():
        conn = get_db_connection()
        if not conn:
            return []
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM products")
                result = cursor.fetchall()
            return result
        finally:
            conn.close()

    @staticmethod
    def get_product_by_id(product_id):
        conn = get_db_connection()
        if not conn:
            return None
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM products WHERE id = %s", (product_id,))
                result = cursor.fetchone()
            return result
        finally:
            conn.close()

    @staticmethod
    def add_product(name, category, quantity, price, description):
        conn = get_db_connection()
        if not conn:
            return False
        try:
            with conn.cursor() as cursor:
                sql = "INSERT INTO products (name, category, quantity, price, description) VALUES (%s, %s, %s, %s, %s)"
                cursor.execute(sql, (name, category, quantity, price, description))
            conn.commit()
            return True
        finally:
            conn.close()

    @staticmethod
    def update_product(product_id, name, category, quantity, price, description):
        conn = get_db_connection()
        if not conn:
            return False
        try:
            with conn.cursor() as cursor:
                sql = "UPDATE products SET name=%s, category=%s, quantity=%s, price=%s, description=%s WHERE id=%s"
                cursor.execute(sql, (name, category, quantity, price, description, product_id))
            conn.commit()
            return True
        finally:
            conn.close()

    @staticmethod
    def delete_product(product_id):
        conn = get_db_connection()
        if not conn:
            return False
        try:
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM products WHERE id = %s", (product_id,))
            conn.commit()
            return True
        finally:
            conn.close()

    @staticmethod
    def add_message(name, email, message):
        conn = get_db_connection()
        if not conn:
            return False
        try:
            with conn.cursor() as cursor:
                sql = "INSERT INTO messages (name, email, message) VALUES (%s, %s, %s)"
                cursor.execute(sql, (name, email, message))
            conn.commit()
            return True
        finally:
            conn.close()

    @staticmethod
    def get_sales_history(product_id):
        conn = get_db_connection()
        if not conn:
            return []
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM sales_history WHERE product_id = %s ORDER BY sale_month ASC", (product_id,))
                result = cursor.fetchall()
            return result
        finally:
            conn.close()

    # ALGORITHM 1: MERGE SORT
    @staticmethod
    def merge_sort(arr, sort_key='name', descending=False):
        if len(arr) > 1:
            mid = len(arr) // 2
            left_half = arr[:mid]
            right_half = arr[mid:]

            ProductModel.merge_sort(left_half, sort_key, descending)
            ProductModel.merge_sort(right_half, sort_key, descending)
            i = j = k = 0
            while i < len(left_half) and j < len(right_half):
                val_left = left_half[i].get(sort_key)
                val_right = right_half[j].get(sort_key)

                if type(val_left) == str:
                    val_left = val_left.lower()
                if type(val_right) == str:
                    val_right = val_right.lower()

                if descending:
                    condition = val_left > val_right
                else:
                    condition = val_left < val_right

                if condition:
                    arr[k] = left_half[i]
                    i += 1
                else:
                    arr[k] = right_half[j]
                    j += 1
                k += 1

            while i < len(left_half):
                arr[k] = left_half[i]
                i += 1
                k += 1

            while j < len(right_half):
                arr[k] = right_half[j]
                j += 1
                k += 1
        return arr

    # ALGORITHM 2: BINARY SEARCH
    @staticmethod
    def binary_search(arr, target_val, search_key='name'):
        """ Assumes arr is already sorted by search_key """
        low = 0
        high = len(arr) - 1
        
        target_val = str(target_val).lower()

        while low <= high:
            mid = (low + high) // 2
            mid_val = str(arr[mid].get(search_key, '')).lower()
            if mid_val == target_val:
                return arr[mid]
            elif mid_val < target_val:
                low = mid + 1
            else:
                high = mid - 1
        
        return None 
