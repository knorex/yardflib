import model

__subclasses__ = ["CC", "CERT", "DC", "DC11", "DOAP", "EXIF", "FOAF", "GEO", "HTTP", "OWL", "RDFS", "RSA", "RSS", "SIOC", "SKOS", "WOT", "XHTML", "XSD"]

def VOCABS():
		for subclass in __subclasses__:
			for v in globals()[subclass]():
				yield v
			
class Vocabulary(object):
	
	__subclasses__ = ["cc", "cert", "dc", "dc11", "doap", "exif", "foaf", "geo", "http", "owl", "rdfs", "rsa", "rss", "sioc", "skos", "wot", "xhtml", "xsd"]

	def __init__(self):
		self.idx = -1

	@property
	def __prefix__(self):
		return self.__class__.__name__.lower()

	def __iter__(self):
		return self

	def next(self):
		if self.idx == len(self.__properties__) - 1:
			raise StopIteration
		self.idx += 1
		self.property = self.__properties__[self.idx]
		return self

	def __str__(self):
		return str(self.uri)

	def vocabs(self):
		for p in self.__properties__:
			yield p
		
	def to_uri(self):
		return model.URI.intern(str(self.uri))	

	@classmethod
	def get_prop(self, v):
		return model.URI.intern(''.join([str(self.uri),str(v)]))

	
class CC(Vocabulary):

    uri = "http://creativecommons.org/ns#"
    __properties__ = ['attributionName','attributionURL','deprecatedOn','jurisdiction','legalcode','license','morePermissions','permits','prohibits','requires']


class CERT(Vocabulary):

    uri = "http://www.w3.org/ns/auth/cert#"
    __properties__ = ['decimal','hex','identity','public_key']


class DC(Vocabulary):

    uri = "http://purl.org/dc/terms/"
    __properties__ = ['abstract','accessRights','accrualMethod','accrualPeriodicity','accrualPolicy','alternative','audience','available','bibliographicCitation','conformsTo','contributor','coverage','created','creator','date','dateAccepted','dateCopyrighted','dateSubmitted','description','educationLevel','extent','format','hasFormat','hasPart','hasVersion','identifier','instructionalMethod','isFormatOf','isPartOf','isReferencedBy','isReplacedBy','isRequiredBy','isVersionOf','issued','language','license','mediator','medium','modified','provenance','publisher','references','relation','replaces','requires','rights','rightsHolder','source','spatial','subject','tableOfContents','temporal','title','type','valid']


class DC11(Vocabulary):

    uri = "http://purl.org/dc/elements/1.1/"
    __properties__ = ['contributor','coverage','creator','date','description','format','identifier','language','publisher','relation','rights','source','subject','title','type']


class DOAP(Vocabulary):

    uri = "http://usefulinc.com/ns/doap#"
    __properties__ = ['anon-root','audience','blog','browse','bug-database','category','created','description','developer','documenter','download-mirror','download-page','file-release','helper','homepage','implements','language','license','location','mailing-list','maintainer','module','name','old-homepage','os','platform','programming-language','release','repository','revision','screenshots','service-endpoint','shortdesc','tester','translator','vendor','wiki']


class EXIF(Vocabulary):

    uri = "http://www.w3.org/2003/12/exif/ns#"
    __properties__ = ['_unknown','apertureValue','artist','bitsPerSample','brightnessValue','cfaPattern','colorSpace','componentsConfiguration','compressedBitsPerPixel','compression','contrast','copyright','customRendered','datatype','date','dateAndOrTime','dateTime','dateTimeDigitized','dateTimeOriginal','deviceSettingDescription','digitalZoomRatio','exifAttribute','exifVersion','exif_IFD_Pointer','exifdata','exposureBiasValue','exposureIndex','exposureMode','exposureProgram','exposureTime','fNumber','fileSource','flash','flashEnergy','flashpixVersion','focalLength','focalLengthIn35mmFilm','focalPlaneResolutionUnit','focalPlaneXResolution','focalPlaneYResolution','gainControl','geo','gpsAltitude','gpsAltitudeRef','gpsAreaInformation','gpsDOP','gpsDateStamp','gpsDestBearing','gpsDestBearingRef','gpsDestDistance','gpsDestDistanceRef','gpsDestLatitude','gpsDestLatitudeRef','gpsDestLongitude','gpsDestLongitudeRef','gpsDifferential','gpsImgDirection','gpsImgDirectionRef','gpsInfo','gpsInfo_IFD_Pointer','gpsLatitude','gpsLatitudeRef','gpsLongitude','gpsLongitudeRef','gpsMapDatum','gpsMeasureMode','gpsProcessingMethod','gpsSatellites','gpsSpeed','gpsSpeedRef','gpsStatus','gpsTimeStamp','gpsTrack','gpsTrackRef','gpsVersionID','height','ifdPointer','imageConfig','imageDataCharacter','imageDataStruct','imageDescription','imageLength','imageUniqueID','imageWidth','interopInfo','interoperabilityIndex','interoperabilityVersion','interoperability_IFD_Pointer','isoSpeedRatings','jpegInterchangeFormat','jpegInterchangeFormatLength','length','lightSource','make','makerNote','maxApertureValue','meter','meteringMode','mm','model','oecf','orientation','photometricInterpretation','pictTaking','pimBrightness','pimColorBalance','pimContrast','pimInfo','pimSaturation','pimSharpness','pixelXDimension','pixelYDimension','planarConfiguration','primaryChromaticities','printImageMatching_IFD_Pointer','recOffset','referenceBlackWhite','relatedFile','relatedImageFileFormat','relatedImageLength','relatedImageWidth','relatedSoundFile','resolution','resolutionUnit','rowsPerStrip','samplesPerPixel','saturation','sceneCaptureType','sceneType','seconds','sensingMethod','sharpness','shutterSpeedValue','software','spatialFrequencyResponse','spectralSensitivity','stripByteCounts','stripOffsets','subSecTime','subSecTimeDigitized','subSecTimeOriginal','subjectArea','subjectDistance','subjectDistanceRange','subjectLocation','subseconds','tag_number','tagid','transferFunction','userComment','userInfo','versionInfo','whiteBalance','whitePoint','width','xResolution','yCbCrCoefficients','yCbCrPositioning','yCbCrSubSampling','yResolution']


class FOAF(Vocabulary):

    uri = "http://xmlns.com/foaf/0.1/"
    __properties__ = ['account','accountName','accountServiceHomepage','age','aimChatID','based_near','birthday','currentProject','depiction','depicts','dnaChecksum','familyName','family_name','firstName','fundedBy','geekcode','gender','givenName','givenname','holdsAccount','homepage','icqChatID','img','interest','isPrimaryTopicOf','jabberID','knows','lastName','logo','made','maker','mbox','mbox_sha1sum','member','membershipClass','msnChatID','myersBriggs','name','nick','openid','page','pastProject','phone','plan','primaryTopic','publications','schoolHomepage','sha1','skypeID','status','surname','theme','thumbnail','tipjar','title','topic','topic_interest','weblog','workInfoHomepage','workplaceHomepage','yahooChatID']


class GEO(Vocabulary):

    uri = "http://www.w3.org/2003/01/geo/wgs84_pos#"
    __properties__ = ['lat','location','long','lat_long']


class HTTP(Vocabulary):

    uri = "http://www.w3.org/2006/http#"
    __properties__ = ['abs_path','absoluteURI','authority','body','connectionAuthority','elementName','elementValue','fieldName','fieldValue','header','param','paramName','paramValue','request','requestURI','response','responseCode','version']


class OWL(Vocabulary):

    uri = "http://www.w3.org/2002/07/owl#"
    __properties__ = ['allValuesFrom','annotatedProperty','annotatedSource','annotatedTarget','assertionProperty','backwardCompatibleWith','bottomDataProperty','bottomObjectProperty','cardinality','complementOf','datatypeComplementOf','deprecated','differentFrom','disjointUnionOf','disjointWith','distinctMembers','equivalentClass','equivalentProperty','hasKey','hasSelf','hasValue','imports','incompatibleWith','intersectionOf','inverseOf','maxCardinality','maxQualifiedCardinality','members','minCardinality','minQualifiedCardinality','onClass','onDataRange','onDatatype','onProperties','onProperty','oneOf','priorVersion','propertyChainAxiom','propertyDisjointWith','qualifiedCardinality','sameAs','someValuesFrom','sourceIndividual','targetIndividual','targetValue','topDataProperty','topObjectProperty','unionOf','versionIRI','versionInfo','withRestrictions']


class RDFS(Vocabulary):

    uri = "http://www.w3.org/2000/01/rdf-schema#"
    __properties__ = ['comment','domain','isDefinedBy','label','member','range','seeAlso','subClassOf','subPropertyOf']


class RSA(Vocabulary):

    uri = "http://www.w3.org/ns/auth/rsa#"
    __properties__ = ['modulus','private_exponent','public_exponent']


class RSS(Vocabulary):

    uri = "http://purl.org/rss/1.0/"
    __properties__ = ['description','items','link','name','title','url']


class SIOC(Vocabulary):

    uri = "http://rdfs.org/sioc/ns#"
#    uri = "http://rdfs.org/sioc/types#"
    __properties__ = ['about','account_of','administrator_of','attachment','avatar','container_of','content','content_encoded    # @deprecated','created_at         # @deprecated','creator_of','description        # @deprecated','earlier_version','email','email_sha1','feed','first_name         # @deprecated','follows','function_of','group_of ','has_administrator','has_container','has_creator','has_discussion','has_function','has_group','has_host','has_member','has_moderator','has_modifier','has_owner','has_parent','has_part ','has_reply','has_scope','has_space','has_subscriber','has_usergroup','host_of','id','ip_address','last_activity_date','last_item_date','last_name','last_reply_date','later_version','latest_version','link','links_to','member_of','moderator_of','modified_at        # @deprecated','modifier_of','name','next_by_date','next_version','note','num_authors','num_items','num_replies','num_threads','num_views','owner_of','parent_of','part_of  ','previous_by_date','previous_version','reference','related_to','reply_of','scope_of','sibling','space_of','subject  ','subscriber_of','title    ','topic','usergroup_of']


class SKOS(Vocabulary):

    uri = "http://www.w3.org/2004/02/skos/core#"
    __properties__ = ['altLabel','broadMatch','broader','broaderTransitive','changeNote','closeMatch','definition','editorialNote','exactMatch','example','hasTopConcept','hiddenLabel','historyNote','inScheme','mappingRelation','member','memberList','narrowMatch','narrower','narrowerTransitive','notation','note','prefLabel','related','relatedMatch','scopeNote','semanticRelation','topConceptOf']


class WOT(Vocabulary):

    uri = "http://xmlns.com/wot/0.1/"
    __properties__ = ['assurance','encryptedTo','encrypter','fingerprint','hasKey','hex_id','identity','length','pubkeyAddress','sigdate','signed','signer','sigtime']


class XHTML(Vocabulary):

    uri = "http://www.w3.org/1999/xhtml#"
    __properties__ = []


class XSD(Vocabulary):

    uri = "http://www.w3.org/2001/XMLSchema#"
    __properties__ = ['NOTATION','QName','anyURI','base64Binary','boolean','date','dateTime','decimal','double','duration','float','gDay','gMonth','gMonthDay','gYear','gYearMonth','hexBinary','string','time','ENTITIES','ENTITY','ID','IDREF','IDREFS','NCName','NMTOKEN','NMTOKENS','Name','byte','int','integer','language','long','negativeInteger','nonNegativeInteger','nonPositiveInteger','normalizedString','positiveInteger','short','token','unsignedByte','unsignedInt','unsignedLong','unsignedShort']