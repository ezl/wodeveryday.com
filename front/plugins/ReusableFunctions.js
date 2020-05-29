import Vue from "vue"

Vue.prototype.$generateBreadcrumb = (store, routeParams, itemTitle = "") => {
  if (itemTitle === "") {
    store.commit("SET_GLOBAL_BREADCRUMB_NAMES", [])
    store.commit("SET_GLOBAL_BREADCRUMB_PATHS", [])
    return
  }

  const pages = Object.keys(routeParams)
  const currentPage = pages.indexOf(itemTitle)
  let breadcrumbNames = ["Home"]
  let breadcrumbPaths = ["/"]
  let path = "/"
  let name = ""
  let cleanedPath = ""

  for (let i = 0; i <= currentPage; i++) {
    name = store.state["current_" + pages[i]]

    if (name != store.state.constants.NOSTATE) {
      breadcrumbNames.push(name)
    } else {
      // if path has NOSTATE then the last path is invalid
      // and should be removed.
      breadcrumbPaths.pop()
    }

    path = path + name + "/"
    cleanedPath = encodeURI(path.toLowerCase().replace(/ /gi, "-"))
    breadcrumbPaths.push(cleanedPath)
  }

  store.commit("SET_GLOBAL_BREADCRUMB_NAMES", breadcrumbNames)
  store.commit("SET_GLOBAL_BREADCRUMB_PATHS", breadcrumbPaths)
}

Vue.prototype.$retrievePathVariables = (store, routeParams) => {
  for (var [key, value] of Object.entries(routeParams)) {
    if (store.state[`current_${key}`] != undefined) continue
    const preparedPathVar = value.replace(/-/gi, " ")
    store.commit(`SET_CURRENT_${key.toUpperCase()}`, preparedPathVar)
  }
}

Vue.prototype.$findParent = (registryObject, name) => {
  registryObject = Object.entries(registryObject)
  let parentName = registryObject.find(
    (parent) => parent[1].indexOf(name) !== -1
  )
  return parentName[0]
}

Vue.prototype.$pushCleanedRoute = ($router, route) => {
  const cleanedRoute = encodeURI(route.toLowerCase().replace(/ /gi, "-"))
  $router.push(cleanedRoute)
}
