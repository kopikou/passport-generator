<script setup lang="ts">
import {computed, onBeforeMount, ref, watch, watchEffect} from "vue";
import {api} from "boot/axios";
import {LocalStorage, SessionStorage, useQuasar} from "quasar";
import {GeneratorListData} from "src/types";
import {useRouter} from "vue-router";
import {storeToRefs} from "pinia";
import _ from "lodash";
import useMainStore from "stores/mainStore";
import LayoutHCF from "components/LayoutHCF.vue";
import useProfActivityViewStore from "stores/profActivityViewStore";
import FileUploader from "pages/upload/components/FileUploader.vue";
import QSelectFilterable from "components/QSelectFilterable.vue";

const $q = useQuasar()
const router = useRouter()

const mainStore = useMainStore();
const profActivityViewStore = useProfActivityViewStore();

const {
  admissionDataProfActivity,
  currentItem,
} = storeToRefs(profActivityViewStore)


watchEffect(() => {
  router.push(`/activity/${currentItem.value}`)
})

</script>

<template>

<div class="q-pa-md">
    <q-layout view="hHh Lpr lff" container style="height: 1000px" >
      <q-header elevated :class="$q.dark.isActive ? 'bg-primary' : 'bg-black'">

      </q-header>

      <q-drawer
        show-if-above
        :width="200"
        :breakpoint="500"

      >
        <q-scroll-area class="fit">
          <q-list style="overflow-y: auto" bordered separator class="q-pa-none">
            <q-item v-for="(item) in admissionDataProfActivity"
                    clickable
                    v-ripple
                    @click="currentItem = item.id"
                    :active="currentItem == item.id"
                    active-class="bg-amber-2 text-black"
            >
        <q-item-section avatar>
          <q-icon name="mdi-text-box-outline" />
        </q-item-section>
        <q-item-section >
          {{ item.abbrprofile}} {{item.startyear }}
        </q-item-section>
      </q-item>
          </q-list>
        </q-scroll-area>
      </q-drawer>

      <q-page-container>
        <q-page padding class="q-pt-none">

          <router-view />

        </q-page>
      </q-page-container>
    </q-layout>
  </div>
</template>

<style scoped lang="scss">
.prof-activity-container {
  display: grid;
  gap: 8px;
  grid-template-columns: repeat(auto-fit, minmax(340px, 1fr));
  padding: 1rem;
}
</style>
