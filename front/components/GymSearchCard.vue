<template>
  <v-app id="inspire">
    <navbar />
    <v-content>
      <breadcrumb :breadcrumb-names="$store.state.globalBreadcrumbNames" />
      <v-row align="center" justify="center" style="flex-direction: column;">
        <v-col cols="12" sm="8" md="4">
          <v-card class="pa-4 elevation-12 ma-4">
            <h1 style="text-align: center;">
              Gyms in {{ $store.state.current_city }}
            </h1>
          </v-card>
        </v-col>
      </v-row>
      <v-row justify="center" class="ma-4">
        <v-col
          v-for="(gymObject, index) in gymList"
          :key="index"
          cols="12"
          xs="12"
          sm="4"
          md="4"
          lg="3"
        >
          <v-item
            v-slot:default="{ active, toggle }"
            @change="selectItem(gymObject)"
          >
            <v-card
              class="mx-auto"
              max-width="344"
              :color="active ? 'primary' : ''"
              @click="toggle"
            >
              <v-img :src="gymObject.photo" height="200px" />
              <v-card-title>
                {{ gymObject.name }}
              </v-card-title>
            </v-card>
          </v-item>
        </v-col>
      </v-row>
    </v-content>
  </v-app>
</template>

<script>
import Navbar from "~/components/Navbar.vue"
import Breadcrumb from "~/components/Breadcrumb.vue"

export default {
  name: "GymSearchCard",
  components: {
    Navbar,
    Breadcrumb,
  },
  props: {
    cardTitle: {
      type: String,
      required: false,
      default: undefined,
    },
    itemTitle: {
      type: String,
      required: false,
      default: undefined,
    },
    itemKey: {
      type: String,
      required: false,
      default: "",
    },
    isLoading: {
      type: Boolean,
      required: false,
      default: true,
    },
    backButtonEnabled: {
      type: Boolean,
      required: false,
      default: false,
    },
    customBackButtonEnabled: {
      type: Boolean,
      required: false,
      default: false,
    },
    gymList: {
      type: Array,
      required: false,
      default: undefined,
    },
    selectItem: {
      type: Function,
      default: () => {},
    },
    selectSubitem: {
      type: Function,
      default: () => {},
    },
  },
  data() {
    return {
      selectedItem: undefined,
    }
  },
  methods: {
    flat(input, depth = 1, stack = []) {
      for (let item of input) {
        if (item instanceof Array && depth > 0) {
          this.flat(item, depth - 1, stack)
        } else {
          stack.push(item)
        }
      }

      return stack
    },
    checkForItemKey() {
      if (this.itemKey.length > 0) {
        return {
          itemText: this.itemKey,
        }
      }
      return []
    },
    navigateBack() {
      if (this.$store.state.current_state === "none") {
        this.$router.go(-2)
      } else {
        this.$router.go(-1)
      }
    },
  },
}
</script>
