import requests

'''
ServerJars API Wrapper For Python3
---------------------------------
Made by bentunadeyilim1234
'''

url = "https://serverjars.com/api/"
endpoints = {
  "downloadJars": "fetchJar/{type}/{category}/{version}",
  "latestDetails": "fetchLatest/{type}/{category}",
  "allDetails": "fetchAll/{type}/{category}/{max}",
  "jarTypes": "fetchTypes/{type}",
  "jarDetails": "fetchDetails/{type}/{category}/{version}"
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

def GetAvailableTypes(type=""):
  if type:
    return _api("jarTypes", "Could not get available types", type=type)[type]
  return _api("jarTypes", "Could not get available types", type=type)

_availabletypes = GetAvailableTypes()

def GetAvailableCategories():
  return [x for x in _availabletypes]

def _findtypebycategory(category: str):
  for type in _availabletypes:
    if category in _availabletypes[type]:
      return type
  return None

class _category:
  def __init__(self, type: str, category: str):
    self.type = (_findtypebycategory(category) if type == "" else type)
    self.category = category
    if not self.type:
      raise SystemExit("Could not find type of category: '{}'".format(self.category))
    if not category in _availabletypes[self.type]:
      raise SystemExit("Could not find category '{}' on type: '{}'".format(self.category, self.type))
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
  def __init__(self, type: str=None):
    if type and type not in _availabletypes:
      raise SystemExit("Could not find type: '{}'".format(type))
    self.type = type
  def Category(self, category: str):
    type = self.type or ""
    return _category(type, category)
  def GetVersions(self, category: str, max: int=None):
    return self.Category(category).GetVersions(max)
  def GetDetails(self, category: str, version: str):
    return self.Category(category).GetDetails(version)
  def GetLatestDetails(self, category: str):
    return self.Category(category).GetLatestDetails()
  def Download(self, category: str, version: str=None, fileName: str=None):
    self.Category(category).Download(version, fileName)
  def DownloadLatest(self, category: str, fileName: str=None):
    self.Category(category).DownloadLatest(fileName)
