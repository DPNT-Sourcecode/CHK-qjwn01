
class HelloSolution:
    
    # friend_name = unicode string
    def hello(self, friend_name = None):
        if friend_name is None or friend_name == "":
            return "Hello, World!"
        return f"Hello, {str(friend_name)}!"

