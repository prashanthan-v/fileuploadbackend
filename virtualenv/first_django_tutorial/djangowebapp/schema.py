from .models import Students
from .models import File
import graphene
from graphene_django import DjangoObjectType
from graphene_file_upload.scalars import Upload


# defining type in schema by mapping to model
class Studenttype(DjangoObjectType):
    class Meta:
        model = Students
        fields ="__all__"
class Filetype(DjangoObjectType):
    class Meta:
        model = File
        fields="__all__"       

# defining mutation in schema

class CreateStudent(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        age = graphene.Int(required=True)

    student = graphene.Field(Studenttype)   

    def mutate(self,info,name,age):
        newStudent = Students(name=name,age=age)
        newStudent.save()
        return CreateStudent(newStudent)
    

class UpdateStudent(graphene.Mutation):
    class Arguments:
        id  = graphene.ID(required=True)  
        name = graphene.String()
        age = graphene.Int()
    updatedstudent = graphene.Field(Studenttype) 
    def mutate(self,info,name,age,id):
        studenttoupdate = Students.objects.get(id=id)
        if name is not None:
          studenttoupdate.name = name
        if age is not None:
            studenttoupdate.age = age  

        studenttoupdate.save()
        return UpdateStudent(studenttoupdate)    

class DeleteStudents(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    success = graphene.Boolean()

    def mutate(self, info, id):
        try:
            Studenttodelete = Students.objects.get(id=id)

            Studenttodelete.delete()
            return DeleteStudents(success=True)  # Return a Boolean value
        except Students.DoesNotExist:
            raise Exception("Student not found")



class SaveFile(graphene.Mutation):
    class Arguments:
        name =graphene.String(required=True)
        file = Upload(required=True)
    success = graphene.Boolean()    
    file= graphene.Field(Filetype)
    def mutate(self, info, file, name):
      uploaded_file = File.objects.create(name=name, file=file)
      return SaveFile(success=True, file=uploaded_file)
    

class GetStudents(graphene.ObjectType):
    students = graphene.List(Studenttype)  
    def resolve_students(self,info):
        return Students.objects.all()   

class Mutation(graphene.ObjectType):
    create_student = CreateStudent.Field()
    update_student = UpdateStudent.Field()
    delete_student = DeleteStudents.Field()     
    save_file      = SaveFile.Field()   


schema = graphene.Schema(query=GetStudents, mutation=Mutation)    