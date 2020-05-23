import Vue from "vue"

Vue.prototype.$generateBreadcrumb = (store, itemTitle = "") => {
  let pages = ["continent", "country", "state", "city"]
  let currentPage = pages.indexOf(itemTitle)
  if (currentPage != -1) {
    let breadcrumbNames = ["Home"]
    for (let i = 0; i <= currentPage; i++) {
      let name = store.state["current_" + pages[i]]
      if (name != store.state.constants.NOSTATE) breadcrumbNames.push(name)
    }
    store.commit("SET_GLOBAL_BREADCRUMB_NAMES", breadcrumbNames)
  } else {
    store.commit("SET_GLOBAL_BREADCRUMB_NAMES", [])
  }
}

Vue.prototype.$retrievePathVariables = (store, routeParams) => {
  for (var [key, value] of Object.entries(routeParams)) {
    if (store.state[`current_${key}`] != undefined) continue
    let preparedPathVar = value.replace(/-/gi, " ")
    console.log(key, value)
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
