import base64
from django.core.files.base import ContentFile
from .models import Students

from graphene_django import DjangoObjectType
import graphene
from graphene_file_upload.scalars import Upload  # Import Upload from graphene-file-upload
from .models import File
from graphene import ObjectType, Boolean, String, Field




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



# class SaveFile(graphene.Mutation):
#     class Arguments:
#         name =graphene.String(required=True)
#         file = Upload(required=True)
#     success = graphene.Boolean()    
#     file= graphene.Field(Filetype)
#     def mutate(self, info, file, name):
#       uploaded_file = File.objects.create(name=name, file=file)
#       return SaveFile(success=True, file=uploaded_file)


# class SaveFile(graphene.Mutation):
#     class Arguments:
#         name = graphene.String(required=True)
#         file = Upload(required=True)  # Expect file as Upload type
    
#     success = graphene.Boolean()
#     file = graphene.Field(Filetype)

#     def mutate(self, info, name, file):
#         try:
#             # Save the uploaded file
#             uploaded_file = File.objects.create(name=name, file=file)
#             return SaveFile(success=True, file=uploaded_file)
#         except Exception as e:
#             print(f"Error: {str(e)}")
#             return SaveFile(success=False, file=None)


# class SaveFile(graphene.Mutation):
#     class Arguments:
#         name = graphene.String(required=True)
#         file = graphene.String(required=True)  # File as a base64-encoded string

#     success = graphene.Boolean()
#     file = graphene.Field(Filetype)

#     def mutate(self, info, name, file):
#         try:
#             # Decode the base64 file string back to binary data
#             file_data = base64.b64decode(file.split(',')[1])  # Handle potential data URL prefix
#             content_file = ContentFile(file_data)

#             # Save the file in the database
#             uploaded_file = File.objects.create(name=name, file=content_file)
#             return SaveFile(success=True, file=uploaded_file)

#         except Exception as e:
#             print(f"Error: {str(e)}")
#             return SaveFile(success=False, file=None)
    

class SaveFile(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        file = graphene.String(required=True)  # Base64 string

    success = graphene.Boolean()
    file = graphene.Field(Filetype)

    def mutate(self, info, name, file):
        try:
            # Decode the base64 file string back to binary data
            file_data = base64.b64decode(file)
            # Create a new File instance
            uploaded_file = File.objects.create(name=name, file=file)
            return SaveFile(success=True, file=uploaded_file)
        except Exception as e:
            print(f"Error: {str(e)}")
            return SaveFile(success=False, file=None)


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