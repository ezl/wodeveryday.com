import apiLibrary from "./../store/apiLibrary.js"

const baseFindPath = "/find"

export default {
  pushCleanedPath(routes, path) {
    path = path.toLowerCase().replace(/ /gi, "-")
    routes.push(path)
    return routes
  },
  async getAppRoutes() {
    // Initiate axios
    let routes = [baseFindPath]
    const url = `${process.env.BACKEND_URL}/affiliates/continents`
    let continentsAndCountries = await apiLibrary.retrieveContinents(url)

    for (let continentName of Object.keys(continentsAndCountries)) {
      routes = this.pushCleanedPath(routes, `${baseFindPath}/${continentName}`)
      let countries = continentsAndCountries[continentName]
      for (let countryName of countries) {
        routes = this.pushCleanedPath(
          routes,
          `${baseFindPath}/${continentName}/${countryName}`
        )
        if (
          ["United States", "Australia", "Canada"].indexOf(countryName) === -1
        ) {
          routes = await this.getCitiesOfCountry(
            continentName,
            countryName,
            routes
          )
        } else {
          routes = await this.getStatesOfCountry(
            continentName,
            countryName,
            routes
          )
        }
      }
    }

    routes = await this.getGymRoutes(routes)

    // Return all available routes
    return routes
  },
  async getGymRoutes(routes) {
    const url = `${process.env.BACKEND_URL}/affiliates/slugs/`
    let gymNameSlugs = await apiLibrary.retrieveCities(url)

    for (let nameSlug of gymNameSlugs) {
      routes.push(`/gym/${nameSlug}`)
    }

    return routes
  },
  async getCitiesOfCountry(continentName, countryName, routes) {
    const country = countryName
    const url = `${process.env.BACKEND_URL}/affiliates/gyms/?country=${country}`
    let citiesAndGyms = await apiLibrary.retrieveCities(url)

    for (let cityName of Object.keys(citiesAndGyms)) {
      routes = this.pushCleanedPath(
        routes,
        `${baseFindPath}/${continentName}/${countryName}/${cityName}`
      )
    }

    return routes
  },
  async getStatesOfCountry(continentName, countryName, routes) {
    const country = countryName
    const url = `${process.env.BACKEND_URL}/affiliates/states/?country=${country}`
    let statesAndCities = await apiLibrary.retrieveStates(url)

    for (let stateName of Object.keys(statesAndCities)) {
      routes = this.pushCleanedPath(
        routes,
        `${baseFindPath}/${continentName}/${countryName}/${stateName}`
      )
      routes = await this.getCitiesOfState(
        continentName,
        countryName,
        stateName,
        routes
      )
    }

    return routes
  },
  async getCitiesOfState(continentName, countryName, stateName, routes) {
    const state = stateName
    const url = `${process.env.BACKEND_URL}/affiliates/gyms/?state=${state}`
    let citiesAndGyms = await apiLibrary.retrieveCities(url)

    for (let cityName of Object.keys(citiesAndGyms)) {
      routes = this.pushCleanedPath(
        routes,
        `${baseFindPath}/${continentName}/${countryName}/${stateName}/${cityName}`
      )
    }

    return routes
  },
}
