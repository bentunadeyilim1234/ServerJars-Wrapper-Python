import requests

'''
ServerJars API Wrapper For Python3
---------------------------------
Made by bentunadeyilim1234
'''

url = "https://serverjars.com/api/"
endpoints = {
  "downloadJars": "fetchJar/{category}/{type}/{version}",
  "latestDetails": "fetchLatest/{category}/{type}",
  "allDetails": "fetchAll/{category}/{type}/{max}",
  "jarTypes": "fetchTypes/{category}",
  "jarDetails": "fetchDetails/{category}/{type}/{version}"
}

def _endpoint(*args, **kwargs):
  return url+endpoints[args[0]].format_map(kwargs)

session = requests.Session()

def _api(*args, **kwargs):
  request = None
  try:
    request = session.get(_endpoint(*args, **kwargs)).json()
  except:
    pass
  if request and request["status"] == "success":
    return request["response"]
  raise SystemExit("There was an error while processing your request"+(" | "+args[1] if args[1] != "" else "."))

def GetAvailableTypes(category=""):
  if category:
    return _api("jarTypes", "Could not get available types", category=category)[category]
  return _api("jarTypes", "Could not get available types", category=category)

_availablecategories = GetAvailableTypes()

def GetAvailableCategories():
  return [x for x in _availablecategories]

def _findcategorybytype(type: str):
  typeslist = _availablecategories
  for category in typeslist:
    if type in typeslist[category]:
      return category
  return None

class _type:
  def __init__(self, category: str, type: str):
    self.category = (_findcategorybytype(type) if category == "" else category)
    self.type = type
    if not self.category:
      raise SystemExit("Could not find category of type: '{}'".format(self.type))
    if not type in _availablecategories[self.category]:
      raise SystemExit("Could not find type '{}' on category: '{}'".format(self.type, self.category))
  def GetVersions(self, max: int=None):
    max = max or ""
    return _api("allDetails", "Could not get versions", type=self.type, category=self.category, max=str(max))
  def GetLatestDetails(self):
    return _api("latestDetails", "Could not get latest details", type=self.type, category=self.category)
  def GetDetails(self, version: str=None):
    if not version or version == "latest":
      version = self.GetLatestDetails()["version"]
    return _api("jarDetails", "Could not get details of version: {}".format(version), type=self.type, category=self.category, version=version)
  def Download(self, version: str=None, fileName: str=None):
    if not version or version == "latest":
      version = self.GetLatestDetails()["version"]
    versionFileName = self.GetDetails(version)["file"]
    if not fileName:
      fileName = versionFileName
    if not fileName.endswith(".jar"):
      fileName = fileName + ".jar"
    if "{}" in fileName:
      fileName = fileName.format(versionFileName)
    downloadUrl = _endpoint("downloadJars", type=self.type, category=self.category, version=version.lower())
    versionDownload = session.get(downloadUrl, allow_redirects=True)
    with open(fileName, 'wb') as file:
      file.write(versionDownload.content)
  def DownloadLatest(self, fileName: str=None):
    latestVersion = self.GetLatestDetails()["version"]
    self.Download(latestVersion, fileName)

class Client:
  def __init__(self, category: str=None):
    self.category = category
    if category and category not in _availablecategories:
      raise SystemExit("Could not find category: '{}'".format(category))
  def Type(self, type: str):
    category = self.category or ""
    return _type(category, type)
  def GetVersions(self, type: str, max: int=None):
    return self.Type(type).GetVersions(max)
  def GetDetails(self, type: str, version: str):
    return self.Type(type).GetDetails(version)
  def GetLatestDetails(self, type: str):
    return self.Type(type).GetLatestDetails()
  def Download(self, type: str, version: str=None, fileName: str=None):
    self.Type(type).Download(version, fileName)
  def DownloadLatest(self, type: str, fileName: str=None):
    self.Type(type).DownloadLatest(fileName)