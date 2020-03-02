from flask import render_template, make_response
import discover.pamac as pamac
from datetime import datetime, timedelta

get = pamac.Get()


def get_categories():
    return {'title': 'Featured', 'href': ''},\
           {'title': 'Applications', 'href': 'applications'},\
           {'title': 'Packages', 'href': 'packages'},\
           {'title': 'Snaps', 'href': 'snaps'}, \
           {'title': 'Flatpaks', 'href': 'flatpaks'}


def get_appstream_app_list(category):
    return get.appstream_category(category)


def appstream_template(category):
    template = "featured.html"
    description = "Discover and explore any Software available in Manjaro linux, supports native application search, packages, snaps and flatpacks."
    apps = get_appstream_app_list(category)
    return render_template(template, apps=apps, nav=get_categories(), title=category, description=description)


def pkgs_template(title):

    template = f"{title.lower()}.html"
    description = f"Discover {title.lower()} available on Manjaro linux."
    apps = get.all_repo_pkgs(title)
    return render_template(template, apps=apps, nav=get_categories(), title=title, total=len(apps), description=description)


def external_repos_template(title):

    template = f"{title.lower()}.html"
    description = f"Discover {title.lower()} available on Manjaro linux."
    categories = get.external_repos()[0]
    pamac_database = get.external_repos()[1]
    return render_template(template, categories=categories, nav=get_categories(), title=title, database=pamac_database, description=description)


def template_404():
    title = "YOU ARE LOST"
    return render_template('404.html', nav=get_categories(), title=title)


def search_package_template(pkg_name, pkg_format):

    pkg = get.search_single_package(pkg_name, pkg_format)
    if not pkg:
        return template_404()        

    title = pkg.get_app_name()
    if not title:
        title = pkg.get_name()

    description = pkg.get_long_desc()
    if not description:
        description = pkg.get_desc()

    template = f"single-{pkg_format.lower()}.html"
    return render_template(template, nav=get_categories(), pkg=pkg, title=title, pkg_format=pkg_format, description=description)


def sitemap_template():
    urls = []
    thirty_days_ago = datetime.now() - timedelta(days=30)
  
    for category in get_categories():
        urls.append([f"https://discover.manjaro.org/{category['href']}", thirty_days_ago])

    for category in "Applications", "Packages":
        packages = get.all_repo_pkgs(category)
        for package in packages:
            urls.append([f"https://discover.manjaro.org/{category.lower()}/{package.get_name()}", thirty_days_ago])
    
    for repo in "Snaps", "flatpaks":
        for category in get.external_repos()[0]:
            database = get.external_repos()[1]
            if repo == "Flatpaks":
                pkg_format = database.get_category_flatpaks(category)                
            elif repo == "Snaps":
                 pkg_format = database.get_category_snaps(category)

            for app in pkg_format:
                 urls.append([f"https://discover.manjaro.org/{repo.lower()}/{app.get_name()}", thirty_days_ago])
            
            
    sitemap_template = render_template('sitemap_template.xml', urls=urls)
    response = make_response(sitemap_template)
    response.headers["Content-Type"] = "application/xml"
    return response