from src.controller import Controller
from src.model import Model
from src.view import View


def setup(view: View, controller: Controller, model: Model):
    view.set_controller(controller)
    model.set_controller(controller)
    controller.set_view(view)
    controller.set_model(model)

def main():
    view = View()
    controller = Controller()
    model = Model()

    setup(view, controller, model)
    view.run()

if __name__ == "__main__":
    main()