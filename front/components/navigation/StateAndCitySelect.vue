<template>
  <geography-search-page
    :item-list="$store.state.states"
    :select-item="selectState"
    :select-subitem="selectCity"
    :item-title="itemTitle"
  />
</template>

<script>
import GeographySearchPage from "~/components/navigation/GeographySearchPage.vue"
import _ from "lodash"

export default {
  name: "StateAndCitySelect",
  components: {
    GeographySearchPage,
  },
  data() {
    return {
      itemTitle: "country",
      metaTags: [],
    }
  },
  computed: {
    fetchPageTitle: function () {
      return this.$store.state.constants.GEO_PAGE_TITLE.replace(
        "{}",
        _.capitalize(this.$route.params[this.itemTitle]).replace(/-/gi, " ")
      )
    },
  },
  mounted() {
    this.metaTags = this.$generateMetaTags(
      this.$store,
      this.fetchPageTitle,
      this.$store.state.constants.DEFAULT_META_DESCRIPTION,
      this.$store.state.constants.DEFAULT_GYM_THUMBNAIL
    )
  },
  methods: {
    selectState(stateName) {
      this.$pushCleanedRoute(this.$router, `${stateName}/`)
    },
    selectCity(stateName, cityName) {
      this.$pushCleanedRoute(this.$router, `${stateName}/${cityName}/`)
    },
  },
  head() {
    return {
      title: this.fetchPageTitle,
      meta: this.metaTags,
    }
  },
}
</script>
