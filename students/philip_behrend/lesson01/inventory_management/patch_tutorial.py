def get_user_input():
    name = input('Enter name : ')
    last_name = input('Enter last name: ')
    age = int(input('Enter age: '))
    robot = input('Are you a robot: ')

    if robot.lower() == 'n':
        return f"You are {name} {last_name}, age {age}"
    if robot.lower() == 'y':
        return f"Welcome my artificial friend"
    return f"You are not human or robot"

if __name__ == '__main__':
    print(get_user_input())