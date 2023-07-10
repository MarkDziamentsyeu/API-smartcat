# API-smartcat
Example of interaction with API smartcat


Official documentation:
https://developers.smartcat.com/getting-started/#smartcat-cli


First you need to initialize the creation of a configuration file config_dict.txt.

The values are passed in double quotes after the colon as in the example
If it is possible to pass multiple values, the values are passed in square brackets and in double quotes
For example targetLanguages: ["ru", "en"]
If the parameter does not need to be passed, we pass null without quotes. For example ClientID: null
Null cannot be passed in name, source Language, targetLanguages, ServiceType.

PROJECT PARAMETERS:
name: "Test"                                      #Project name. We pass in double quotes
sourceLanguage: "en"                                     #The source language of the project
targetLanguages: ["ru"]                                  #Project translation languages. If there are several languages, then pass in square brackets, in double quotes separated by commas                                                                    ["ru","de"]
deadline: "2023-04-04T14:15:00+03:00"                    #Project deadline. If not necessary, we pass null without buckets
description: "Project Description"                       #Project description. If not necessary, we pass null without buckets
workflowStages: ["translation", "editing"]               #Stages of the project workflow. If not necessary, we pass null without quotes. You can transfer several. In square brackets, double quotes                                                    separated by commas. There are:(Translation, Editing, Proofreading, Postediting, FinalPageProof, Notarization, CertifiedTranslation,                                                                 Transcreation, Legalization, PreliminaryPageProof)

externalTag: "12345678"                                   #Tag of the external system. If not necessary we pass null
ClientID: null                                            #client ID.
creatorUserId: null                                       #ID of the project creator(manager). If not necessary we pass null
file_path: "data/example.docx "                           #The path to the file. We pass it in single quotes, without a space after the colon. If the document is missing, pass null
id_TM: null                                               #id translation memory that we want to add. If not necessary we pass null
glossary: null                                            #Glossary list, you can pass several in square brackets and double quotes separated by commas 
                                                            ["18a9fc46-2674-4fef-aac4-6c50571ed99f","d878ad27-7828-450e-b2cd-7f0492c24d86"]. If not necessary we pass null



DOCUMENT PARAMETERS:
externalId: "123456789"                                     #External identifier assigned by the client when creating the document, If not necessary, we pass null



LINGUIST SEARCH PARAMETERS

ServiceType: "Translation"                                   #The type of freelancer services is: Translation, Editing, Proofreading, Postediting, PageProof, GlossaryCreation,                                                                                     SimultaneousTranslation, ConsecutiveTranslation, MediaTranslation, ExpertReview, projectmanagement, TranslationMemoryCreation,                                                                       Copywriting, Training, Transcription, Notarization, CertifiedTranslation , Transcreation, Legalization

targetLanguage_lingvist: "en"                                 #Translation language. a parameter for searching for a linguist. You can pass null then in the my_team file.json displays all                                                                         available linguists whose sourceLanguage is equal to the specified value

specializations: ["Education"]                                # The translator's specialization is: Education, ProductsAndCatalogs, DocumentsAndCertificates, Marketing, Correspondence, Software,                                                                    Fiction, ScienceAndPatents, ContractsAndReports, Gaming, Manuals, Website, AnnualReport, CorporateAndSocialResponsibility,                                                                           TechnicalAndEngineering, Cryptocurrencies, Biochemistry, Computingscience, Electronics, Metallurgy , Nuclear, Optics, Printing,                                                                      Telecommunication, Textile, Patent, Military, EcologyAndEnvironment, Agriculture, ArtsAndCulture, AviationAndSpace, Biology,                                                                         Cartography, Chemistry, Cosmetics, Construction, Architecture, Economics, Accounting, BankingAndInvestment, Insurance, Energy,                                                                       ThermalPowerEngineering, MechanicalEngineering, Finance, General, Geography, Geology, Mining, History, Linguistics, Philosophy,                                                                      Psychology, Sociology, Industry, IndustrialAutomation, ElectricalEngineering, IT, ERP, Law, HR, Mathematics, Medicine,                                                                               MedicalEquipment, Pharmaceutics, VeterinaryMedicine, OilAndGas, Physics, PoliticsAndSociety, RealEstate, Recreation, Fashion,                                                                        LuxuryItems, TourismAndTravel, Religion, SocialScience, Sport, Transport, AutomotiveBusiness, FoodAndDrinks, Biotechnology,                                                                          Business, LifeSciences
                                                                you can transfer several. You can pass null. then in the my_team file.json displays all available linguists, including those who do                                                                   not have a specialization.

id_lingvist: null                                               #Here we pass the id of the linguist. If not necessary, we pass null



