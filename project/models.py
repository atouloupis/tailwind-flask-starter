from flask_login import UserMixin
from . import db
import enum,datetime

class user(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(1000))
    name = db.Column(db.String(1000))
    dateOfBirth = db.Column(db.Date())
    phone1=db.Column(db.String(100))
    phone2=db.Column(db.String(100))

#    Fournisseurs = db.relationship('fournisseur', backref='user')
    UserProfileResidences = db.relationship('userprofileresidence', backref='user')
    files = db.relationship('files', backref='user')
    sinister = db.relationship('sinister', backref='user')
    quote = db.relationship('quote', backref='user')
    invoice = db.relationship('invoice', backref='user')
    appartment = db.relationship('appartment', backref='user')
    userSinisterImpacted = db.relationship('usersinisterimpacted', backref='user')
    message = db.relationship('message', backref='user')
    

class residence(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    number = db.Column(db.Integer)
    street=db.Column(db.String(1000))
    type=db.Column(db.String(100))
    city=db.Column(db.String(1000))
    x=db.Column(db.Integer)
    y=db.Column(db.Integer)
    idBan=db.Column(db.String(100),nullable=False)
    label=db.Column(db.String(1000))
    postcode=db.Column(db.Integer)
    insee=db.Column(db.Integer)
    complement=db.Column(db.String(1000))
    lotSize=db.Column(db.Integer)
    tantieme=db.Column(db.Integer)
    dpe=db.Column(db.String(10))
    dpeLink=db.Column(db.String(1000))
    dtgLink=db.Column(db.String(1000))
    dtgResume=db.Column(db.String(1000))
    heatingSystem=db.Column(db.String(100))
    financeId=db.Column(db.Integer,db.ForeignKey('finance.id'))
    elevators=db.Column(db.Integer)
    yearOfConstruction=db.Column(db.Integer)

    FournisseurResidence = db.relationship('fournisseurresidence', backref='residence')
    UserProfileResidence = db.relationship('userprofileresidence', backref='residence')
    Appartement = db.relationship('appartment', backref='residence')
    filesresidence = db.relationship('filesresidence', backref='residence')

class profile(enum.Enum):
    fournisseur="Fournisseur"
    syndic="Syndic Professionel"
    gestionnaire="Gestionnaire"
    admin="Administrateur"
    coproprietaire="Copropriétaire"
    conseiller="Conseiller Syndical"
    president="Président"

class userprofileresidence(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    userId=db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
    residenceId=db.Column(db.Integer,db.ForeignKey('residence.id'),nullable=False)
    profile=db.Column(db.Enum(profile))
    isActive=db.Column(db.Integer)

    messageRecipient = db.relationship('messagerecipient', backref='userprofileresidence')

class fournisseur(UserMixin, db.Model): 
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    companyName=db.Column(db.String(100))
    siren=db.Column(db.Integer)
    siret=db.Column(db.Integer)
    adress=db.Column(db.String(1000))
    idBan=db.Column(db.String(100))
    health=db.Column(db.Integer)
    idGoogle=db.Column(db.String(100))
    rateGoogle=db.Column(db.Integer)
    reviewNumbers=db.Column(db.Integer)
    tvaIntracommunautaire=db.Column(db.String(100))
    mail=db.Column(db.String(100))
    phone1=db.Column(db.String(100))
    phone2=db.Column(db.String(100))
    userId=db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
    financeId=db.Column(db.Integer,db.ForeignKey('finance.id'),nullable=False)

    quotes = db.relationship('quote', backref='fournisseur')
    activiteFournisseur = db.relationship('activitefournisseur', backref='fournisseur')
    FournisseurResidence = db.relationship('fournisseurresidence', backref='fournisseur')
    charges = db.relationship('charges', backref='fournisseur')

class activite(enum.Enum):
    plombier="Plombier"
    electicien="Electricien"
    peinture="Peintre"
    grosOeuvre="Gros Oeuvre"
    menuiserie="Menuiserie"
    telecom="Telecomunication"
    fournisseurElec="Fournisseur d'electricité"
    distributeurEau="Distributeur d'eau"
    chauffagiste="Chauffagiste"
    autre="Autre"


class activitefournisseur(UserMixin, db.Model):    
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    fournisseurId=db.Column(db.Integer,db.ForeignKey('fournisseur.id'),nullable=False)
    activite=db.Column(db.Enum(activite))

class fournisseurresidence(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    fournisseurId=db.Column(db.Integer,db.ForeignKey('fournisseur.id'),nullable=False)
    residenceId=db.Column(db.Integer,db.ForeignKey('residence.id'),nullable=False)

class fileType(enum.Enum):
    facture="Facture"
    quote="Estimation"
    rib="Rib"
    test="Test"

class files(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True,nullable=False) # primary keys are required by SQLAlchemy
    storageId=db.Column(db.String(200),unique=True,nullable=False)
    userUpload = db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
    uploadDate = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    fileType = db.Column(db.Enum(fileType))
    metadataFile = db.Column(db.String(1000))

    invoices = db.relationship('invoice', backref='files')
    message = db.relationship('message', backref='files')
    finance = db.relationship('finance', backref='files')
    filesresidence = db.relationship('filesresidence', backref='files')


class filesresidence(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True,nullable=False) # primary keys are required by SQLAlchemy
    filesId=db.Column(db.Integer,db.ForeignKey('files.id'))
    residenceId=db.Column(db.Integer,db.ForeignKey('residence.id'))
    
class invoice(UserMixin, db.Model):
    id= db.Column(db.Integer, primary_key=True,nullable=False) # primary keys are required by SQLAlchemy
    fileId=db.Column(db.Integer,db.ForeignKey('files.id'),nullable=False)
    totalPriceWithVAT= db.Column(db.Integer,unique=True,nullable=False)
    paid=db.Column(db.Boolean) #oui non
    creatorId=db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)

    invoicesinister= db.relationship('invoicesinister', backref='invoice')

class quoteStatus(enum.Enum):
    en_cours="En cours"
    termine="Terminé"

class quoteType(enum.Enum):
    sinistre="Sinistre"
    travaux="Travaux"
    entretient="Entretient"
    amelioration="Amélioration"

class quote(UserMixin, db.Model):
    id= db.Column(db.Integer, primary_key=True,nullable=False) # primary keys are required by SQLAlchemy
    quoteType= db.Column(db.Enum(quoteType))#sinistre, travaux, entretient, ...
    status= db.Column(db.Enum(quoteStatus))
    reccurent=db.Column(db.Boolean) #true false
    engagementInMonths=db.Column(db.Integer,nullable=False)
    fournisseurId = db.Column(db.Integer,db.ForeignKey('fournisseur.id'),nullable=False)
    residenceId= db.Column(db.Integer,nullable=False)
    totalPriceWithVAT= db.Column(db.Integer,nullable=False)
    totalPrice= db.Column(db.Integer,nullable=False)
    userCreator=db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)

    quoteLines = db.relationship('quotelines', backref='quote')
    quotesinister = db.relationship('quotesinister', backref='quote')


class unit(enum.Enum):
    squaremeter="Metres carrés"
    linearmeter="Metres linéaires"
    liter="Litre"
    metrecube="Metres cubes"
    kg="Kilogrammes"
    unit="Unité"

class quoteLinesStatus(enum.Enum):
    accept="Accepté"
    tovalidate="A valider"


class quotelines(UserMixin, db.Model):
    id= db.Column(db.Integer, primary_key=True,nullable=False) # primary keys are required by SQLAlchemy
    quoteId= db.Column(db.Integer,db.ForeignKey('quote.id'),nullable=False)
    lineName = db.Column(db.String(100),nullable=False)
    description = db.Column(db.String(500),nullable=False)
    linePrice= db.Column(db.Integer,unique=True,nullable=False)
    VAT= db.Column(db.Integer,unique=True,nullable=False)
    quantity= db.Column(db.Integer,unique=True,nullable=False)
    unit=db.Column(db.Enum(unit))
    status=db.Column(db.Enum(quoteLinesStatus))


class appartment(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True,nullable=False) # primary keys are required by SQLAlchemy
    userId= db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
    residenceId=db.Column(db.Integer,db.ForeignKey('residence.id'),nullable=False)
    lotNumber=db.Column(db.String(10))
    tantieme= db.Column(db.Integer,unique=True,nullable=False)
    number= db.Column(db.String(5),nullable=False)
    area= db.Column(db.Integer,unique=True,nullable=False)
    dpe=db.Column(db.String(1),nullable=False)
    dpeResume=db.Column(db.String(500),nullable=False)

class bankList(enum.Enum):
    creditmutuel="Credit Mutuel"
    qonto="Qonto"
    bnpPro="BNP Professionel"
    helloBanque="Hello Banque"

class finance(UserMixin, db.Model):
    id= db.Column(db.Integer, primary_key=True,nullable=False) # primary keys are required by SQLAlchemy
    ribId= db.Column(db.Integer,db.ForeignKey('files.id'),nullable=False)
    iban= db.Column(db.String(20),nullable=False)
    bank=db.Column(db.Enum(bankList))

    Residence = db.relationship('residence', backref='finance')
    Fournisseur= db.relationship('fournisseur', backref='finance')

class sinisterType(enum.Enum):
    water="Dégat des eaux"
    fire="Incendie"
    natural="Catastrophe naturelle"
    weather="Intempérie"
    cambriolage="Cambriolage"
    brisDeGalce="Bris de glace"
    travaux="Travaux"
    autre="Autre"

class sinisterStatus(enum.Enum):
    new="Nouveau"
    inProgess="En cours de traitement"
    work="En travaux"
    over="Terminé"

class sinister(UserMixin, db.Model):
    id= db.Column(db.Integer, primary_key=True,nullable=False) # primary keys are required by SQLAlchemy
    floor= db.Column(db.Integer,unique=True,nullable=False)
    stairs= db.Column(db.String(20),nullable=False)
    sinisterType=db.Column(db.Enum(sinisterType))
    status=db.Column(db.Enum(sinisterStatus))
    description= db.Column(db.String(500),nullable=False)
    creatorId= db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
    createdDate=db.Column(db.DateTime())

    userSinisterImpacted= db.relationship('usersinisterimpacted', backref='sinister')
    invoicesinister= db.relationship('invoicesinister', backref='sinister')
    quotesinister = db.relationship('quotesinister', backref='sinister')


class usersinisterimpacted(UserMixin, db.Model):
    id= db.Column(db.Integer, primary_key=True,nullable=False) # primary keys are required by SQLAlchemy
    userId= db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
    sinisterId= db.Column(db.Integer,db.ForeignKey('sinister.id'),nullable=False)

class quotesinister(UserMixin, db.Model):
    id= db.Column(db.Integer, primary_key=True,nullable=False) # primary keys are required by SQLAlchemy
    quoteId= db.Column(db.Integer,db.ForeignKey('quote.id'),nullable=False)
    sinisterId= db.Column(db.Integer,db.ForeignKey('sinister.id'),nullable=False)

class invoicesinister(UserMixin, db.Model):
    id= db.Column(db.Integer, primary_key=True,nullable=False) # primary keys are required by SQLAlchemy
    invoiceId= db.Column(db.Integer,db.ForeignKey('invoice.id'),nullable=False)
    sinisterId= db.Column(db.Integer,db.ForeignKey('sinister.id'),nullable=False)


class travaux(UserMixin, db.Model):
    id= db.Column(db.Integer, primary_key=True,nullable=False) # primary keys are required by SQLAlchemy


class charges(UserMixin, db.Model):
    id= db.Column(db.Integer, primary_key=True,nullable=False) # primary keys are required by SQLAlchemy
    fournisseurId= db.Column(db.Integer,db.ForeignKey('fournisseur.id'),nullable=False)
    periodicity= db.Column(db.String(2),nullable=False)
    totalPriceWithVAT= db.Column(db.Integer,unique=True,nullable=False)
    endDate=db.Column(db.Date())
    startDate=db.Column(db.Date())
    
class appeldecharge(UserMixin, db.Model):
    id= db.Column(db.Integer, primary_key=True,nullable=False) # primary keys are required by SQLAlchemy
    description= db.Column(db.String(500),nullable=False)
    totalPriceWithVAT= db.Column(db.Integer,unique=True,nullable=False)



class message(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True,nullable=False) # primary keys are required by SQLAlchemy
    filesId= db.Column(db.Integer,db.ForeignKey('files.id'),nullable=False) #table
    subject= db.Column(db.String(100),nullable=False)
    creatorId= db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
    messageBody= db.Column(db.String(1000),nullable=False)
    createDate=db.Column(db.DateTime())
    parentMessageId=db.Column(db.Integer)
    expiryDate=db.Column(db.Date())
    isReminder=db.Column(db.Boolean)
    nextReminderDate=db.Column(db.Date())
    #reminderFrequencyId= db.Column(db.Integer,db.ForeignKey('reminder.id'),nullable=False)

    messageRecipient = db.relationship('messagerecipient', backref='message')


class messagerecipient(UserMixin, db.Model):
    id= db.Column(db.Integer, primary_key=True,nullable=False) # primary keys are required by SQLAlchemy
    recipientId= db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
    UserProfileResidenceId= db.Column(db.Integer,db.ForeignKey('userprofileresidence.id'))
    messageId= db.Column(db.Integer,db.ForeignKey('message.id'),nullable=False)
    isRead=db.Column(db.Boolean)




