<template>
  <v-row
    align="center"
    justify="center"
    style="flex-direction: row; width: 80%;"
  >
    <v-col cols="8">
      <v-autocomplete
        v-model="selectedItem"
        :items="getSearchableList"
        :loading="isLoading"
        color="white"
        hide-no-data
        hide-selected
        placeholder="Search for a Gym"
        return-object
        @change="selectSubitemPrefetch(null, selectedItem)"
      />
    </v-col>
    <v-col>
      <v-autocomplete
        v-model="selectedItem"
        :items="getSearchableList"
        :loading="isLoading"
        color="white"
        hide-no-data
        hide-selected
        placeholder="Search for a location"
        return-object
        @change="selectSubitemPrefetch(null, selectedItem)"
      />
    </v-col>
  </v-row>
</template>

<script>
export default {
  name: "GeographySearchBar",
  props: {
    itemList: {
      type: Object,
      required: false,
      default: Object,
    },
    selectSubitemPrefetch: {
      type: Function,
      default: () => {},
    },
  },
  data() {
    return {
      selectedItem: undefined,
    }
  },
  computed: {
    getSearchableList: function () {
      if (!this.itemList) return []
      let searchableList = this.flat(Object.values(this.itemList))
      return searchableList
    },
    isLoading: function () {
      return (
        this.itemList === undefined || Object.values(this.itemList).length === 0
      )
    },
  },
  methods: {
    flat(input, depth = 1, stack) {
      const validStack = stack || []
      for (let item of input) {
        if (item instanceof Array && depth > 0) {
          this.flat(item, depth - 1, validStack)
        } else {
          // TODO: remove this tech debt
          if (item && typeof item !== "string") item = item[0]
          validStack.push(item)
        }
      }

      return validStack
    },
  },
}
</script>
