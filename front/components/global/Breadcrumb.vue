<template>
  <v-card-text>
    <h3
      v-for="(name, index) in breadcrumbNames"
      :key="index"
      class="text-uppercase d-inline-block"
    >
      <nuxt-link :to="breadcrumbPaths[index] || ''">
        <v-btn text>
          {{ name }}
        </v-btn>
      </nuxt-link>
      <span v-if="index != breadcrumbNames.length - 1" class="px-2">
        >
      </span>
    </h3>
  </v-card-text>
</template>

<script>
export default {
  name: "Breadcrumb",
  data() {
    return {
      breadcrumbNames: [],
      breadcrumbPaths: [],
    }
  },
  computed: {
    onGymPage: function () {
      return this.$route.fullPath.indexOf("/gym/") !== -1
    },
  },
  mounted() {
    if (this.onGymPage) {
      this.generateBreadCrumbFromGym()
    } else {
      this.generateBreadCrumb()
    }
  },
  methods: {
    generateBreadCrumb() {
      const routeParams = this.$route.params
      const pageNames = Object.values(routeParams)
      const pages = Object.keys(routeParams)
      const pageCount = pages.length - 1

      if (pageCount === -1) return

      this.populateBreadcrumb(pageNames, pageCount)
    },
    generateBreadCrumbFromGym() {
      const continent = this.$store.state.gym_object.continent
      const country = this.$store.state.gym_object.country
      const state = this.$store.state.gym_object.full_state
      const city = this.$store.state.gym_object.city
      let breadCrumbList = [continent, country, city]
      if (state) breadCrumbList.splice(2, 0, state)

      this.populateBreadcrumb(breadCrumbList, breadCrumbList.length - 1)
    },
    populateBreadcrumb(nameList, iterations) {
      this.breadcrumbNames = ["Home"]
      let path = "/find/"
      this.breadcrumbPaths = ["/"]
      let name = ""
      let cleanedPath = ""

      for (let i = 0; i <= iterations; i++) {
        name = nameList[i]
        path = path + name + "/"
        cleanedPath = encodeURI(path.toLowerCase().replace(/ /gi, "-"))
        this.breadcrumbPaths.push(cleanedPath)
        this.breadcrumbNames.push(name.replace(/-/gi, " "))
      }
    },
  },
}
</script>
