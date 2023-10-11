from labs.grading import Default


class ExerciseSource(Default):
    __LAB__ = "exercise-source"

    def start(self):
        print("Hello World!")

    def finish(self):
        print("This is the finish function from '{}'".format(self.__LAB__))
