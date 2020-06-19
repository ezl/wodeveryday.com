<template>
  <div>
    <navbar />
    <breadcrumb
      :breadcrumb-names="$store.state.global_bread_crumb_names"
      :breadcrumb-paths="$store.state.global_bread_crumb_paths"
    />
    <gym-navbar
      :navbar-active="navbarActive"
      :goto-elements="$store.state.gym_navbar_goto_elements"
      :navbar-options="$store.state.gym_navbar_options"
    />
    <v-row>
      <v-col v-show="windowInnerWidth > 540">
        <info-card class="mb-3" />
        <reviews-card
          :id="windowInnerWidth > 540 ? 'reviews' : ''"
          class="mb-3"
        />
      </v-col>
      <v-col id="keyInfo">
        <info-card v-show="windowInnerWidth <= 540" class="mb-3" />
        <contact-info-card class="mb-3" />
        <hours-card class="mb-3" />
        <price-card class="mb-3" />
        <address-card class="mb-3" :gym-address="gymAddress" />
        <reviews-card
          v-show="windowInnerWidth <= 540"
          :id="windowInnerWidth <= 540 ? 'reviews' : ''"
          class="mb-3"
        />
      </v-col>
    </v-row>
    <v-row>
      <v-col>
        <span id="photos">
          <photo-grid id="photoGrid" />
          <photo-carousel />
        </span>
        <leaderboard-card
          v-if="$store.state.gym_object.name"
          id="leaderboard"
        />
        <map-card :gym-address="gymAddress" />
      </v-col>
    </v-row>
  </div>
</template>

<script>
import Navbar from "~/components/global/Navbar.vue"
import Breadcrumb from "~/components/global/Breadcrumb.vue"
import InfoCard from "~/components/gym_page/InfoCard.vue"
import PhotoCarousel from "~/components/gym_page/PhotoCarousel.vue"
import MapCard from "~/components/gym_page/MapCard.vue"
import HoursCard from "~/components/gym_page/HoursCard.vue"
import ReviewsCard from "~/components/gym_page/ReviewsCard.vue"
import LeaderboardCard from "~/components/gym_page/LeaderboardCard.vue"
import PhotoGrid from "~/components/gym_page/PhotoGrid.vue"
import ContactInfoCard from "~/components/gym_page/ContactInfoCard.vue"
import AddressCard from "~/components/gym_page/AddressCard.vue"
import GymNavbar from "~/components/gym_page/GymNavbar.vue"
import PriceCard from "~/components/gym_page/PriceCard.vue"
import apiLibrary from "~/store/apiLibrary.js"

export default {
  components: {
    Navbar,
    Breadcrumb,
    InfoCard,
    ContactInfoCard,
    AddressCard,
    PhotoGrid,
    PhotoCarousel,
    MapCard,
    HoursCard,
    ReviewsCard,
    LeaderboardCard,
    GymNavbar,
    PriceCard,
  },
  async fetch({ route, store }) {
    if (store.state.gym_object.name === undefined) {
      const country = route.params["country"].replace(/-/gi, " ")
      const state = route.params["state"].replace(/-/gi, " ")
      const city = route.params["city"].replace(/-/gi, " ")
      const gymName = route.params["gym"].replace(/-/gi, " ")
      let url = `${process.env.BACKEND_URL}/affiliates/?name__iexact=${gymName}&city__iexact=${city}&country__iexact=${country}`
      if (state != store.state.constants.NOSTATE)
        url += `&full_state__iexact=${state}`

      url = encodeURI(url)
      await apiLibrary.retrieveGym(url, store)
    }
  },
  data() {
    return {
      gymAddress: undefined,
      navbarOptions: ["Key Info"],
      gotoElements: ["#keyInfo"],
      navbarActive: false,
      windowInnerWidth: 0,
    }
  },
  computed: {
    fetchGymSearchQuery: function () {
      const query =
        this.$store.state.gym_object.name +
        " " +
        this.$store.state.gym_object.city +
        " " +
        this.$store.state.gym_object.country
      return query
    },
    fetchGymURL: function () {
      const country = this.$store.state["current_country"]
      const state = this.$store.state["current_state"]
      const city = this.$store.state[`current_city`]
      const gymName = this.$store.state[`current_gym`]
      let url = `${process.env.BACKEND_URL}/affiliates/?name__iexact=${gymName}&city__iexact=${city}&country__iexact=${country}`
      if (state != this.$store.state.constants.NOSTATE)
        url += `&full_state__iexact=${state}`

      url = encodeURI(url)
      return url
    },
    fetchReviewCount: function () {
      if (!this.$store.state.place_details.reviews) return 0
      return this.$store.state.place_details.reviews.length
    },
    fetchPageDescription: function () {
      return `${this.fetchReviewCount} reviews for ${
        this.$store.state[`current_gym`]
      }. Photos, Pricing, Contact Information and All You Need To Know Before Visiting`
    },
    fetchIdPlusJsonScript: function () {
      return JSON.stringify({
        "@context": "https://schema.org",
        "@type": "ExerciseGym",
        name: this.$store.state.gym_object.name,
        image: this.$store.state.gym_object.photo,
        "@id": this.$store.state.gym_object.url,
        address: {
          "@type": "PostalAddress",
          streetAddress: this.$store.state.gym_object.address,
          postalCode: this.$store.state.gym_object.zip,
          addressCountry: this.$store.state.gym_object.country,
        },
      })
    },
  },
  mounted() {
    this.$retrievePathVariables(this.$store, this.$route.params)
    this.$generateBreadcrumb(this.$store, this.$route.params, "gym")

    // empty navbar for refill
    this.$store.commit("SET_GYM_NAVBAR_OPTIONS", [])
    this.$store.commit("SET_GYM_NAVBAR_GOTO_ELEMENTS", [])

    this.gymAddress = this.getAddress()
    const map = this.initMap()
    this.getPlaceDetails(map)
  },
  created() {
    if (process.client) window.addEventListener("resize", this.handleResize)
    this.handleResize()
  },
  destroyed() {
    if (process.client) window.removeEventListener("resize", this.handleResize)
  },
  methods: {
    handleResize() {
      if (process.client) this.windowInnerWidth = window.innerWidth
    },
    fillGymNavbar() {
      let navbarOptions = ["Key Info"]
      let gotoElements = ["#keyInfo"]

      if (
        this.$store.state.place_details.reviews &&
        this.$store.state.place_details.reviews.length > 0
      ) {
        navbarOptions.push("Reviews")
        gotoElements.push("#reviews")
      }

      navbarOptions.push("Map")
      gotoElements.push("#map")

      if (
        this.$store.state.place_details.photos &&
        this.$store.state.place_details.photos.length > 0
      ) {
        navbarOptions.push("Photos")
        gotoElements.push("#photos")
      }

      this.$store.commit("UNSHIFT_TO_GYM_NAVBAR_OPTIONS", navbarOptions)
      this.$store.commit("UNSHIFT_TO_GYM_NAVBAR_GOTO_ELEMENTS", gotoElements)

      this.navbarActive = true
    },
    initMap() {
      apiLibrary.initMap(
        this.$store.state.gym_object.lat,
        this.$store.state.gym_object.lon
      )
    },
    getPlaceDetails(map) {
      var request = {
        query: this.fetchGymSearchQuery,
        fields: ["name", "place_id", "geometry"],
      }

      // eslint-disable-next-line no-undef
      let service = new google.maps.places.PlacesService(map)

      apiLibrary.retrieveGymId(service, request).then((gymId) => {
        var detailsRequest = {
          placeId: gymId,
          fields: [
            "formatted_phone_number",
            "rating",
            "review",
            "photos",
            "opening_hours",
          ],
        }
        apiLibrary
          .retrieveGymDetails(this.$store, service, detailsRequest)
          // eslint-disable-next-line no-unused-vars
          .then((place) => {
            this.fillGymNavbar()
          })
      })
    },
    getAddress() {
      let gymFullAddress = this.$store.state.gym_object.address
      gymFullAddress += ", " + this.$store.state.gym_object.city
      if (this.$store.state.gym_object.full_state)
        gymFullAddress += ", " + this.$store.state.gym_object.full_state
      gymFullAddress += " " + this.$store.state.gym_object.zip
      return gymFullAddress
    },
  },
  head() {
    return {
      title: this.$store.state.gym_object.name,
      __dangerouslyDisableSanitizers: ["script"],
      script: [
        {
          innerHTML: this.fetchIdPlusJsonScript,
          type: "application/ld+json",
        },
      ],
      meta: [
        {
          hid: "description",
          name: "description",
          content: this.fetchPageDescription,
        },
        {
          property: "og:title",
          content: `${this.$store.state.gym_object.name} | WOD Every Day`,
        },
        {
          property: "og:description",
          content: this.fetchPageDescription,
        },
        {
          property: "og:image",
          content: this.$store.state.gym_object.photo,
        },
      ],
    }
  },
}
</script>

<style lang="scss" scoped>
#photoGrid {
  @media (max-width: 960px) {
    display: none;
  }
}
.col {
  padding-top: 0px;
  padding-bottom: 0px;
}
::-webkit-scrollbar {
  width: 10px;
  height: 10px;
}
::-webkit-scrollbar-track {
  background: transparent;
  border: 1px solid darkgray;
  border-radius: 5px;
}
::-webkit-scrollbar-thumb {
  background: #888;
  border-radius: 5px;
}
::-webkit-scrollbar-thumb:hover {
  background: #555;
  border-radius: 5px;
}
</style>
