<script setup lang="ts">

import {onBeforeMount, ref, watch} from "vue";
import dayjs from "dayjs";
import _ from "lodash";
import {useQuasar} from "quasar";
import {api} from "boot/axios";
import {useRouter} from "vue-router";

const $q = useQuasar()
const router = useRouter()

const programList = ref()
const yearsOptions = _.map(Array(dayjs().year() - 2024), (x, i) => {
  return dayjs().year() - i
})

const year = ref($q.localStorage.getItem('scientificPlan_year') ? $q.localStorage.getItem('scientificPlan_year') : dayjs().year())


async function fetchPrograms() {
  let r = await api.get('/api/generator/get-asp-program-list/', {params: {year: year.value}})
  programList.value = r.data
}

function openAspScientificPlan(id) {
  router.push(`/scientific-plan/${id}`)
}

watch(year, async () => {
  $q.loading.show({message: "Загрузка данных"})
  $q.localStorage.set('scientificPlan_year', year.value)
  await fetchPrograms()
  $q.loading.hide()
})

onBeforeMount(async () => {
  $q.loading.show({message: "Загрузка данных"})
  await fetchPrograms()
  $q.loading.hide()
})

</script>

<template>
  <div class="q-pa-lg q-gutter-y-md">
    <div class="text-center text-h6 q-mb-md">Список рабочих программ по программе аспирантуры ИРНИТУ</div>
    <q-select
      label="Выберите учебный год"
      :options="yearsOptions"
      v-model="year"
      outlined
      stack-label
    />
    <div class="q-gutter-y-xs">
      <q-list bordered separator>
          <q-item v-for="item in programList" clickable v-ripple @click="openAspScientificPlan(item.id)">
            <q-item-section>
              <div class="text-subtitle1">{{ item.species }} <span class="text-bold">{{ item.name }}</span></div>
            </q-item-section>
          </q-item>
      </q-list>
    </div>
  </div>
</template>

<style scoped>

</style>
