<script setup lang="ts">

import axios from "axios";
import {onBeforeMount, ref} from "vue";
import PlanView from "components/PlanView.vue";
import DisciplineView from "components/DisciplineView.vue";
import DocumentsView from "components/DocumentsView.vue";
import CompetencesView from "components/CompetencesView.vue";
import IndicatorsView from "components/IndicatorsView.vue";
import SemesterView from "components/SemesterView.vue";
import {useQuasar} from "quasar";

const $q = useQuasar()

const props = defineProps( {
    id: {
    required: true,
    type: Number
  }
})

const link = ref('plan')
const plan_data = ref([])
const lines_data = ref([])
const documents_data = ref([])
const semester_data = ref([])
const indicators_data = ref([])
async function getFileData() {
  $q.loading.show()

  let r = await axios.get("api/upload/get_file_by_id/", {params: {id: props.id}})
    .catch((response) => {
      $q.notify({
        color: 'negative',
        message: 'Ошибка получения данных, перезагрузите страницу',
        icon: 'mdi-alert-box',
        position: 'top',
      })
      $q.loading.hide()
    })

  plan_data.value = r.data.parser[0]
  lines_data.value = r.data.parser[1]
  semester_data.value = r.data.parser[2]
  indicators_data.value = r.data.parser[3]
  documents_data.value = r.data.parser[4]

  $q.loading.hide()
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
          :active="link === 'documents'"
          @click="link = 'documents'"
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
        <plan-view v-if="link === 'plan'" :data="plan_data"/>
        <discipline-view v-if="link === 'disciple'" :data="lines_data"/>
        <documents-view v-if="link === 'documents'" :data="documents_data"/>
        <semester-view v-if="link === 'semester'" :data="semester_data"/>
        <competences-view v-if="link === 'competences'" :data="indicators_data"/>
        <indicators-view v-if="link === 'indicators'" :data="indicators_data"/>
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
