import Vue from "vue"

Vue.prototype.$generateBreadcrumb = (store, itemTitle = "") => {
  console.log("called")
  let pages = ["continent", "country", "state", "city"]
  let currentPage = pages.indexOf(itemTitle)
  if (currentPage != -1) {
    let breadcrumbNames = ["Home"]
    for (let i = 0; i <= currentPage; i++) {
      let name = store.state["current_" + pages[i]]
      if (name != "none") breadcrumbNames.push(name)
    }
    store.commit("SET_GLOBAL_BREADCRUMB_NAMES", breadcrumbNames)
  } else {
    store.commit("SET_GLOBAL_BREADCRUMB_NAMES", [])
  }
}

Vue.prototype.$retrieveStoredPathVariable = (
  pathVarName,
  store,
  routeParams
) => {
  let pathVariable = store.state[`current_${pathVarName}`]
  if (pathVariable === undefined) {
    pathVariable = routeParams[pathVarName]
    store.commit(`SET_CURRENT_${pathVarName.toUpperCase()}`, pathVariable)
  }
  return pathVariable
}

Vue.prototype.$findParent = (registryObject, name) => {
  registryObject = Object.entries(registryObject)
  let parentName = registryObject.find(
    (parent) => parent[1].indexOf(name) !== -1
  )
  return parentName[0]
}
