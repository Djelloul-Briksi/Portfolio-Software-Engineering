''' Main module for the task '''

# standard modules
import sys
import json
import traceback


# own modules
import database
import action


def main():
    ''' Entry point of the program '''

    # open connection to database
    my_database = database.Database()

    # these are the complex action data, which shall come in a request from the Frontend
    ActId = 719
    ActListId = 93
    ActDetId = 1025
    ActTyp = 'CAStatic'
    MedTyp = 'CAStatic'

    # get actions tree of this root action
    root_action = action.Action(ActId, ActListId, ActDetId, ActTyp, MedTyp)
    action_tree = action.getActionTree(root_action, my_database.db_conn)
    my_database.close()

    # dump the tree as json
    with open('cplxaction.json', 'w') as fp:
            json.dump(action_tree, fp, indent=2)

if __name__ == "__main__":
    try:
        main()
        print("\nProgramm ended successfully!\n")

    except database.DatabaseException as e:
        print("\nProgramm ended with a database error:\n\t{}\n".format(str(e)))

    except:
        print("Programm ended with unknown error: see message below")
        exception_type, exception_value, exception_traceback = sys.exc_info()
        print("Exception Type: {}\nException Value: {}".format(exception_type, exception_value))
        file_name, line_number, procedure_name, line_code = traceback.extract_tb(exception_traceback)[-1]
        print("File Name: {}\nLine Number: {}\nProcedure Name: {}\nLine Code: {}".format(file_name, line_number, procedure_name, line_code))
