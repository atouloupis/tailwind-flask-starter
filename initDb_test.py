from project import create_app
from werkzeug.security import generate_password_hash
from datetime import date

# Créez une instance de l'application Flask
app = create_app()

# Activez le contexte d'application
app.app_context().push()

from project.models import user, db, files, residence,finance,bankList,fileType,userprofileresidence,profile

def create_test_data():
    # Créer des utilisateurs de test
    user1 = user(name='Andreas Touloupis', email='andreas.touloupis@gmail.com',password=generate_password_hash('123456', method='pbkdf2'), dateOfBirth=date(1990, 12, 12))
    user2 = user(name='jojo', email='jojo@example.com',password=generate_password_hash('123456', method='pbkdf2'), dateOfBirth=date(1990, 12, 12))

    residence1 = residence(
    label='46 Rue Voltaire 92250 La Garenne-Colombes',
    number= 46,
    idBan= '92035_9670_00046',
    postcode= 92250,
    insee= 92035,
    x= 644978,
    y= 6867404.25,
    city= 'La Garenne-Colombes',
    type= 'housenumber',
    street= 'Rue Voltaire',
    financeId=1
    )

    residence2 = residence(
    label='12 rue du chateau 92000 Neuilly sur Seine',
    number= 12,
    idBan= '92023_9670_00046',
    postcode= 92000,
    insee= 92023,
    x= 644978,
    y= 6867404.25,
    city= 'Neuilly sur Seine',
    type= 'housenumber',
    street= 'Rue du Chateau',
    financeId=1
    )
    
    file1 = files(storageId='https://geduser.blob.core.windows.net/ged-immeuble/RIB (1).pdf', fileName='Premier RIB', userUpload=1,uploadDate=date(2023, 12, 12), fileType=fileType.rib,metadataFile="{content-type:'application/pdf'}")
    finance1= finance(ribId=1,iban='FR76XXXXXXXXXXXX',bank=bankList.creditmutuel)
    userprofileresidence1= userprofileresidence(userId=1,residenceId=1,profile=profile.admin,isActive=1)
    userprofileresidence1= userprofileresidence(userId=1,residenceId=2,profile=profile.coproprietaire,isActive=1)
    userprofileresidence1= userprofileresidence(userId=2,residenceId=1,profile=profile.fournisseur,isActive=1)

    # Ajouter les utilisateurs à la base de données
    db.session.add(user1)
    db.session.add(user2)
    db.session.commit()
    db.session.add(file1)
    db.session.commit()
    db.session.add(finance1)
    db.session.commit()
    db.session.add(residence1)
    db.session.commit()
    db.session.add(residence2)
    db.session.commit()
    db.session.add(userprofileresidence1)
    db.session.commit()
    db.session.add(userprofileresidence2)
    db.session.commit()
     db.session.add(userprofileresidence3)
    db.session.commit()   

    # Committer les changements
    

if __name__ == '__main__':
    create_test_data()