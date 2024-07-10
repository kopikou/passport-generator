<script setup lang="ts">

import axios from "axios";
import {onBeforeMount, ref} from "vue";
import PlanView from "components/PlanView.vue";
import DisciplineView from "components/DisciplineView.vue";
import FilesView from "components/FilesView.vue";
import CompetencesView from "components/CompetencesView.vue";
import IndicatorsView from "components/IndicatorsView.vue";
import SemesterView from "components/SemesterView.vue";

const props = defineProps( {
    id: {
    required: true,
    type: Number
  }
})

const link = ref('plan')

async function getFileData() {
  console.log(props.id)
  let r = await axios.get("api/upload/get_file_by_id/", {params: {id: props.id} })
  console.log(r.data.items)
}

onBeforeMount(() => {
  getFileData()
})

</script>

<template>
<div class="q-pt-md">
  <div class="row">
    <div class="col-2">
      <q-list
      bordered
      >
        <q-item
          clickable
          v-ripple
          :active="link === 'plan'"
          @click="link = 'plan'"
          active-class="my-menu-link"
        >

        <q-item-section avatar>
          <q-icon name="mdi-book-edit-outline" />
        </q-item-section>

        <q-item-section>План</q-item-section>

        </q-item>
        <q-item
          clickable
          v-ripple
          :active="link === 'disciple'"
          @click="link = 'disciple'"
          active-class="my-menu-link"
        >

        <q-item-section avatar>
          <q-icon name="mdi-account-school" />
        </q-item-section>

        <q-item-section>Дисциплины</q-item-section>

        </q-item>
        <q-item
          clickable
          v-ripple
          :active="link === 'files'"
          @click="link = 'files'"
          active-class="my-menu-link"
        >

        <q-item-section avatar>
          <q-icon name="mdi-file-document-outline" />
        </q-item-section>

        <q-item-section>Документы</q-item-section>

        </q-item>
        <q-item
          clickable
          v-ripple
          :active="link === 'semester'"
          @click="link = 'semester'"
          active-class="my-menu-link"
        >

        <q-item-section avatar>
          <q-icon name="mdi-clock-alert-outline" />
        </q-item-section>

        <q-item-section>Семестры</q-item-section>

        </q-item>
        <q-item
          clickable
          v-ripple
          :active="link === 'competences'"
          @click="link = 'competences'"
          active-class="my-menu-link"
        >

        <q-item-section avatar>
          <q-icon name="mdi-text-account" />
        </q-item-section>

        <q-item-section>Компетенции</q-item-section>

        </q-item>
        <q-item
          clickable
          v-ripple
          :active="link === 'indicators'"
          @click="link = 'indicators'"
          active-class="my-menu-link"
        >

        <q-item-section avatar>
          <q-icon name="mdi-invoice-check-outline" />
        </q-item-section>

        <q-item-section>Индикаторы</q-item-section>

        </q-item>
      </q-list>
    </div>
    <div class="col-10">
      <div class="q-pl-lg">
        <plan-view v-if="link === 'plan'" :id="props.id"/>
        <discipline-view v-if="link === 'disciple'" :id="props.id"/>
        <files-view v-if="link === 'files'" :id="props.id"/>
        <semester-view v-if="link === 'semester'" :id="props.id"/>
        <competences-view v-if="link === 'competences'" :id="props.id"/>
        <indicators-view v-if="link === 'indicators'" :id="props.id"/>
      </div>
    </div>
  </div>
</div>
</template>

<style scoped>
.my-menu-link {
  color: white;
  background: #F2C037;
}
</style>
