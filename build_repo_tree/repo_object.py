from abc import ABCMeta, ABC, abstractmethod
from question_seeds import questions_seeds
# class name could be: directory, documentation, configuration_file, bash_script, python_file, python_class etc.
class Repo_tree_object(ABC):
    def __init__(self,parent,class_name,content):
        self.parent = parent
        self.object_class = class_name
        self.content = []

    @abstractmethod
    def parse_content(self):
        pass
    @abstractmethod
    def generate_instance(self):
        pass



class Repo_tree_directory(Repo_tree_object):
    def __init__(self,parent,directory_name,content,name):
        self.parent = parent
        self.name = name
        self.object_class = "directory"
        self.directory_name = directory_name
        self.content = content
        self.children = []

    def __str__(self):
        return f"Repo_object: {self.repo_id}, {self.repo_name}, {self.repo_url}, {self.repo_description}, {self.repo_language}, {self.repo_created_at}, {self.repo_updated_at}, {self.repo_pushed_at}, {self.repo_size}, {self.repo_stargazers_count}, {self.repo_watchers_count}, {self.repo_forks_count}, {self.repo_open_issues_count}, {self.repo_default_branch}"
    def parse_content(self):

        #TODO add all files to children
        self.children.add()
    def generate_instance(self):
        
        for question_seed in questions_seeds[self.object_class]:
            #build question, build answer
            continue
        pass
