<template>
  <div itemscope itemtype="https://schema.org/ExerciseGym">
    <navbar />
    <breadcrumb />
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
        <address-card class="mb-3" />
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
        <map-card />
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
import reusableFunctionsLibrary from "~/store/reusableFunctionsLibrary.js"

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
  async asyncData({ route, store }) {
    store.commit("SET_PLACE_PHOTOS", [])
    const gymNameSlug = route.params["gym_slug"]
    const gymUrl = `${process.env.BACKEND_URL}/gyms/?name_slug__iexact=${gymNameSlug}`
    await apiLibrary.retrieveGym(gymUrl, store)

    const gymSearchQuery = `${store.state.gym_object.name} ${store.state.gym_object.city} ${store.state.gym_object.country}`
    const detailsUrl = `${process.env.BACKEND_URL}/gym_details/?gym_id=${store.state.gym_object.id}&gym_search_query=${gymSearchQuery}`
    await apiLibrary.retrieveGymDetails(detailsUrl, store)

    let reviewCount =
      store.state.place_details.reviews !== undefined
        ? store.state.place_details.reviews.length
        : "0"
    let pageTitle = `${store.state.gym_object.name} | ${store.state.constants.WEBSITE_TITLE}`
    let pageDescription = `${reviewCount} reviews for ${store.state.gym_object.name}. Photos, Pricing, Contact Information and All You Need To Know Before Visiting`

    let metaTags = reusableFunctionsLibrary.generateMetaTags(
      store,
      pageTitle,
      pageDescription,
      store.state.gym_object.photo,
      route.fullPath
    )

    return {
      metaTags: metaTags,
    }
  },
  data() {
    return {
      navbarOptions: ["Key Info"],
      gotoElements: ["#keyInfo"],
      navbarActive: false,
      windowInnerWidth: 0,
      metaTags: [],
    }
  },
  computed: {
    fetchIdPlusJsonScript: function () {
      return JSON.stringify({
        "@context": "https://schema.org",
        "@type": "ExerciseGym",
        name: this.$store.state.gym_object.name,
        image: this.$store.state.gym_object.photo,
        telephone:
          this.$store.state.place_details.international_phone_number || "",
        address: {
          "@type": "PostalAddress",
          streetAddress: this.$store.state.gym_object.address,
          postalCode: this.$store.state.gym_object.zip,
          addressCountry: this.$store.state.gym_object.country,
        },
      })
    },
    checkIfPlaceDetailsHasPhotos: function () {
      return (
        (this.$store.state.place_details.photos &&
          this.$store.state.place_details.photos[0] &&
          this.$store.state.place_details.photos[0].photo_url === undefined) ||
        this.$store.state.place_details.photos === undefined ||
        (this.$store.state.place_details.photos &&
          this.$store.state.place_details.photos.length === 0)
      )
    },
  },
  mounted() {
    // empty navbar for refill
    this.$store.commit("SET_GYM_NAVBAR_OPTIONS", [])
    this.$store.commit("SET_GYM_NAVBAR_GOTO_ELEMENTS", [])
    this.initMap()
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
      apiLibrary
        .initMap(
          this.$store.state.gym_object.lat,
          this.$store.state.gym_object.lon
        )
        .then((map) => {
          if (this.checkIfPlaceDetailsHasPhotos) this.getPlacePhotos(map)
        })
    },
    getPlacePhotos(map) {
      // This function is tech debt to get photos working temporarily.
      // Remove after photos are working
      if (this.$store.state.place_details.place_id) {
        var detailsRequest = {
          placeId: this.$store.state.place_details.place_id,
          fields: ["photos"],
        }

        // eslint-disable-next-line no-undef
        let service = new google.maps.places.PlacesService(map)
        apiLibrary
          .retrieveGymPhotos(this.$store, service, detailsRequest)
          // eslint-disable-next-line no-unused-vars
          .then((result) => {
            this.fillGymNavbar()
            this.updatePlacePhotos()
          })
      }
    },
    updatePlacePhotos() {
      const gymUrl = `${process.env.BACKEND_URL}/gym_details/update_photos/`
      apiLibrary.updateGymDetails(gymUrl, this.$store.state.place_details)
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
      meta: this.metaTags,
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
