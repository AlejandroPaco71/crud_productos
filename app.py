from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///tienda.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# definicion del modelo Product 
class Product(db.Model):
    __tablename__ = "Product"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False, default=0)
    
    def __repr__(self):
        return f"Name: {self.name}  Price: {self.price}  Stock: {self.stock}"


#funcion para iniciar la base dedatos
def init_db():
    with app.app_context():
        db.create_all()
        print("Base de datos con tabla Product creado exitosamente")
        
#Funcion para Inseratar productos 
def insert_product():
    print("\n--- AÑADIR NUEVO PRODUCTO ---\n")
    with app.app_context():
        # Captura de datos
        nombre_prod = input("Ingrese el nombre: ")
        precio_prod = input("Ingrese el precio: ")
        cantidad_prod = input("Ingrese el stock (opcional): ")

        # Validamos si se proporcionaron todos los datos
        if all([nombre_prod, precio_prod, cantidad_prod]):
            nuevo_prod = Product(
                name=nombre_prod, 
                price=float(precio_prod), 
                stock=int(cantidad_prod)
            )
            mensaje = "Producto registrado con exito"
        else:
            # Caso donde el stock queda vacío 
            nuevo_prod = Product(
                name=nombre_prod, 
                price=float(precio_prod)
            )
            mensaje = "Producto guardado (stock predeterminado en 0)."

        # Ejecución de persistencia en la BD
        db.session.add(nuevo_prod)
        db.session.commit()
        print(mensaje)

# Funcion para mostrar todos los productos, por stock agotado y id = 3
def query_products():
    with app.app_context():
        # 1. Listar todo
        print("\n--- TODOS LOS PRODUCTOS ---")
        for i, pro in enumerate(Product.query.all(), 1):
            print(f"[{i}] {pro}")

        # 2. Filtrar sin stock
        print("\n--- AGOTADOS (STOCK 0) ---")
        agotados = Product.query.filter(Product.stock == 0).all()
        for i, pro in enumerate(agotados, 1):
            print(f"[{i}] {pro}")

        # 3. Búsqueda por ID
        print("\n--- BUSCAR POR ID  ---")
        p_id = int(input("ID del producto a mostrar: "))
        prod = Product.query.filter_by(id=p_id).first()
        if prod:
            print(prod)
        else:
            print("Producto No Encontrado!")

#Funcion para actualizar producto
def update_product():
    print("\n--- EDITAR PRODUCTO ---\n")
    with app.app_context():
        # Búsqueda directa por ID
        p_id = input("ID del producto a editar: ")
        item = Product.query.filter_by(id=p_id).first()

        if not item:
            return print("Error: ID no encontrado.")

        # Captura de nuevos datos
        nuevo_nombre = input("Nuevo nombre: ")
        nuevo_precio = input("Nuevo precio: ")
        nuevo_stock = input("Nuevo stock (Enter para 0): ")

        # Actualizamos atributos 
        item.name = nuevo_nombre
        item.price = float(nuevo_precio)
        
        # Si hay valor en nuevo_stock
        if nuevo_stock:
            item.stock = int(nuevo_stock)
        else:
            item.stock = 0

        #Guardamos en la base de datos
        db.session.commit()
        print("Registro actualizado")

#Funcion para eliminar un producto
# Funcion para eliminar un producto existente de la base de datos
def delete_product():
    print("\n--- ELIMINAR PRODUCTO ---\n")
    with app.app_context():
        # Busqueda por el ID
        p_id = int(input("ID del producto a eliminar: "))
        product = Product.query.filter_by(id=p_id).first()
        # Si existe el producto lo eliminamos 
        if product:
            # Lo eliminamos
            db.session.delete(product)
            # Guardamos en la base de datos
            db.session.commit()
            print("Producto eliminado")
        else:
            print("Producto no existe")
            
if __name__ == "__main__":
    #Iniciamos la creacion de la base de datos
    init_db()
    #Un bucle while 
    while True:
        print("\n" + " INVENTARIO DE PRODUCTOS  ".center(50, "="))
        print("1. Añadir | 2. Listar | 3. Editar | 4. Borrar | 5. Salir")
        print("=" * 50)
        
        #Pedimos que ingrese un numero del menu
        opcion = int(input("Seleccione una opción: "))
        
        if opcion == 1:
            insert_product()
        elif opcion == 2:
            query_products()
        elif opcion == 3:
            update_product()
        elif opcion == 4:
            delete_product()
        elif opcion == 5:
            break
        else:
            print("Opción no válida.")
