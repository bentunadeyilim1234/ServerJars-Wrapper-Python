<!-- PROJECT LOGO -->
<div align="center">
  <!--<a href="https://github.com/othneildrew/Best-README-Template">
    <img src="logo.png" alt="Logo" width="80" height="80">
  </a>-->

  <h3 align="center">ServerJars Python Wrapper</h3>

  <p align="center">
    A simple yet flexible and fast Python3 wrapper for ServerJars REST API.
    <br />
    <br />
    <a href="https://github.com/bentunadeyilim1234/ServerJars-Wrapper-Python/issues">Report Bug</a>
    ·
    <a href="https://github.com/bentunadeyilim1234/ServerJars-Wrapper-Python/issues">Request Feature</a>
  </p>
</div>

<!-- USAGE EXAMPLES -->
## Usage
Here is the simple usage list of ServerJars wrapper:
```python
import serverjars as sj

#Initalize Client
client = sj.Client()

#Initalize Type (Optional)
paper = client.Type("paper")

#List Versions (Optional max)
client.GetVersions("paper")
paper.GetVersions(max=5)

#Get Details of Version (Optional version)
client.GetDetails("paper", "latest")
paper.GetDetails()

#Get Details of Latest Version
client.GetLatestDetails("paper")
paper.GetLatestDetails()

#Download (Optional version, fileName)
client.Download("paper", "1.18.2", "downloads/{}")
paper.Download()

#Download Latest (Optional fileName)
client.DownloadLatest("paper", "paper.jar")
paper.Download("latest")
```

<!-- LICENSE -->
## License

Distributed under the GPL 3.0 license. See `LICENSE` for more information.

<!-- CONTACT
## Contact
Your Name - [@your_twitter](https://twitter.com/your_username) - email@example.com
Project Link: [https://github.com/your_username/repo_name](https://github.com/your_username/repo_name)
<p align="right">(<a href="#readme-top">back to top</a>)</p>
-->
