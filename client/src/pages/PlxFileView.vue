<script setup lang="ts">

import {onBeforeMount, ref} from "vue";
import PlanView from "components/PlanView.vue";
import DisciplineView from "components/DisciplineView.vue";
import DocumentsView from "components/DocumentsView.vue";
import CompetencesView from "components/CompetencesView.vue";
import IndicatorsView from "components/IndicatorsView.vue";
import SemesterView from "components/SemesterView.vue";
import {useQuasar} from "quasar";
import _ from "lodash";
import {api} from "boot/axios";

const $q = useQuasar()

const props = defineProps( {
    id: {
    required: true,
  }
})


const link = ref('plan')
const planData = ref([])
const linesData = ref([])
const documentsData = ref([])
const semesterData = ref([])
const indicatorsData = ref([])
async function getFileData() {

  let r = await api.get("api/upload/get-file-by-id/", {params: {id: props.id}})
    .catch((response) => {
      $q.notify({
        color: 'negative',
        message: 'Ошибка получения данных, перезагрузите страницу',
        icon: 'mdi-alert-box',
        position: 'top',
      })
    })

  planData.value = r.data.parser.plan
  linesData.value = r.data.parser.lines
  semesterData.value = r.data.parser.semester
  indicatorsData.value = r.data.parser.indicators
  documentsData.value = r.data.parser.documents

}


onBeforeMount(async() => {
  $q.loading.show()
  await getFileData()
  $q.loading.hide()
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
        <plan-view v-if="link === 'plan'" :data="planData"/>
        <discipline-view v-if="link === 'disciple'" :data="linesData"/>
        <documents-view v-if="link === 'documents'" :data="documentsData"/>
        <semester-view v-if="link === 'semester'" :data="semesterData"/>
        <competences-view v-if="link === 'competences'" :data="indicatorsData"/>
        <indicators-view v-if="link === 'indicators'" :data="indicatorsData"/>
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
