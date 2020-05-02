<template>
  <v-app id="inspire">
    <v-content>
      <v-container class="fill-height" fluid>
        <v-row align="center" justify="center">
          <v-col cols="12" sm="8" md="4">
            <v-card class="pa-4 elevation-12">
              <v-btn
                v-if="backButtonEnabled"
                class="mb-4"
                block
                dark
                @click="$router.go(-1)"
              >
                <!--eslint-disable-next-line vue/singleline-html-element-content-newline-->
                <v-icon left dark> mdi-arrow-left-bold </v-icon>Back
              </v-btn>
              <v-btn
                v-if="customBackButtonEnabled"
                class="mb-4"
                block
                dark
                @click="navigateBack()"
              >
                <!--eslint-disable-next-line vue/singleline-html-element-content-newline-->
                <v-icon left dark> mdi-arrow-left-bold </v-icon>Back
              </v-btn>
              <v-autocomplete
                v-model="selectedItem"
                v-bind="checkForItemKey()"
                :items="itemList"
                :loading="isLoading"
                color="white"
                hide-no-data
                hide-selected
                :label="`Search for a ${itemTitle}`"
                placeholder="Start typing to Search"
                prepend-icon="mdi-dumbbell"
                return-object
                @change="selectItem(selectedItem)"
              />
              <v-card style="max-height: 400px;" class="overflow-y-auto">
                <v-btn
                  v-for="(item, index) in itemList"
                  :key="index"
                  text
                  large
                  @click="selectItem(item)"
                >
                  <span v-if="itemKey.length > 0">
                    {{ item[itemKey] }}
                  </span>
                  <span v-else>
                    {{ item }}
                  </span>
                </v-btn>
              </v-card>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </v-content>
  </v-app>
</template>

<script>
export default {
  name: "SearchCard",
  props: {
    itemTitle: {
      type: String,
      required: false,
      default: "item",
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
    itemList: {
      type: Array,
      required: false,
      default: undefined,
    },
    selectItem: {
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
