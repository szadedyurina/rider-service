import connexion
from connexion.resolver import RestyResolver
from injector import Binder

# def configure(binder: Binder) -> Binder:
#     binder.bind(
#         Database,
#         Database(
#             MongoProvider("http://0.0.0.0", 27017
#             )
#         )
#     )
#
#     return binder


if __name__ == '__main__':
    app = connexion.App(__name__, specification_dir='swagger/')
    app.add_api('app.yaml', resolver=RestyResolver('api'))
    # FlaskInjector(app=app.app, modules=[configure])
    app.run(port=9090)



