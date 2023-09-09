
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
from datetime import datetime


class DatabaseManager:
    _instance = None

    def __new__(cls, uri=None):
        if cls._instance is None:
            cls._instance = super(DatabaseManager, cls).__new__(cls)
            cls._instance.client = MongoClient(uri)
            cls._instance.db = cls._instance.client['user_data']
            cls._instance.students = cls._instance.db['students']
            cls._instance.projects = cls._instance.db['projects']
            cls._instance.universities = cls._instance.db['universities']
            cls._instance.administrators = cls._instance.db['administrators']
        return cls._instance

    @staticmethod
    def insert_administrator(username: str, password: str):
        administrator_data = {
            '_id': str(uuid.uuid4()),
            'username': username,
            'password': generate_password_hash(password=password)
        }
        try:
            DatabaseManager()._instance.administrators.insert_one(administrator_data)
            status = True
        except Exception as error:
            print(str(error))
            status = False
        finally:
            return status

    @staticmethod
    def verify_administrator(username: str, password: str):
        administrator = DatabaseManager()._instance.administrators.find_one({
            'username': username})
        if administrator:
            if check_password_hash(administrator['password'], password):
                return True, administrator
            else:
                return False, 'Incorrect Password'
        else:
            return False, f'No administrator with username - {username}'

    @staticmethod
    def check_administrator(_id: str):
        administrator = DatabaseManager(
        )._instance.administrators.find_one({'_id': _id})
        if administrator:
            return True
        else:
            return False

    @staticmethod
    def insert_university(university_name: str, erp_info: tuple):
        university_data = {
            '_id': str(uuid.uuid4()),
            'name': university_name,
            'erp_info': erp_info,
            'authorized_users': []
        }
        try:
            DatabaseManager()._instance.universities.insert_one(university_data)
            status = True
        except Exception as error:
            print(str(error))
            status = False
        finally:
            return status

    @staticmethod
    def verify_university(username: str, password: str):
        university = DatabaseManager()._instance.universities.find_one({
            'username': username})
        if university:
            if check_password_hash(university['password'], password):
                return True, university
            else:
                return False, 'Incorrect Password'
        else:
            return False, f'No university account with username - {username}'

    @staticmethod
    def get_all_universities():
        try:
            universities = DatabaseManager()._instance.universities.find(
                {}, {"_id": 1, "name": 1})
            university_list = [
                {"_id": university["_id"], "name": university["name"]} for university in universities]
            return university_list
        except Exception as error:
            print(str(error))
            return []

    @staticmethod
    def insert_student(university_id: str, university_username: str, university_password: str):
        student = {
            '_id': str(uuid.uuid4()),
            'university_id': university_id,
            'university_name': DatabaseManager.get_university_by_id(university_id)['name'],
            'university_username': university_username,
            'university_password': generate_password_hash(university_password)
        }
        return DatabaseManager()._instance.students.insert_one(student)

    @staticmethod
    def get_student(_id):
        return DatabaseManager()._instance.students.find_one({'_id': _id})

    @staticmethod
    def check_student(university: str, university_username: str, password: str):
        user = DatabaseManager()._instance.students.find_one({
            'university': university,
            'university_username': university_username
        })
        if user:
            if check_password_hash(user['university_password'], password):
                return True, user
            else:
                return False, 'Incorrect password'
        return False, 'User not found'

    @staticmethod
    def insert_project(student_id: str, project_type: str, branch: str, title: str, description: str):
        student = DatabaseManager.get_student(student_id)
        if student:
            university_id = student_id['university_id']
            university_name = student_id['university_name']
        else:
            return False

        project_data = {
            '_id': str(uuid.uuid4()),
            'upload_time': datetime.now(),
            'title': title,
            'project_type': project_type,
            'branch': branch,
            'description': description,
            'managers': [{
                student_id: [
                    university_id,
                    university_name
                ]
            }],
            'technologies': [],
            'resources': {}
        }
        try:
            DatabaseManager()._instance.projects.insert_one(project_data)
            status = True
        except Exception as error:
            print(str(error))
            status = False
        finally:
            return status

    @staticmethod
    def find_projects(
        university_id: str | None = None,
        branch: str | None = None,
        project_type: str | None = None,
        title: str | None = None,
        student_id: str | None = None,
        university_name: str | None = None,
        technologies: str | None = None
    ):
        query = {}

        if university_id is not None:
            query['university_id'] = university_id

        if branch is not None:
            query['branch'] = branch

        if project_type is not None:
            query['project_type'] = project_type

        if title is not None:
            query['title'] = title

        if student_id is not None:
            query['managers.student_id'] = student_id

        if university_name is not None:
            query['managers.university_name'] = university_name

        if technologies is not None:
            query['technologies'] = {'$in': technologies}
        projects = DatabaseManager()._instance.projects.find(query)
        return list(projects)

    @staticmethod
    def add_student_to_project(project_id, student_id):
        try:
            project = DatabaseManager()._instance.projects.find_one(
                {'_id': project_id})
            if project:
                if student_id not in project['team']:
                    student = DatabaseManager.get_student(student_id)
                    if student:
                        project['managers'].append(
                            {student_id: [student['university_id'], student['university_name']]})
                        DatabaseManager()._instance.projects.update_one(
                            {'_id': project_id},
                            {'$set': {'team': project['team'],
                                      'managers': project['managers']}}
                        )
                        status = True
                    else:
                        status = False, 'Invalid Student Id'
                else:
                    status = False, 'Student is already in the team'
            else:
                status = False, 'Project not found'
        except Exception as error:
            print(str(error))
            status = False, str(error)
        finally:
            return status

    # @staticmethod
    # def remove_manager(project_id: str, manager_id: str):
    #     try:
    #         DatabaseManager()._instance.projects.update_one(
    #             {'_id': project_id},
    #             {'$pull': {'managers': manager_id}}
    #         )
    #         status = True
    #     except Exception as error:
    #         print(str(error))
    #         status = False
    #     finally:
    #         return status

    def close_connections(self):
        self.client.close()
