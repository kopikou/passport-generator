<script setup lang="ts">


import {ref, onBeforeMount, computed} from "vue";
import api from "axios"
import _ from "lodash";
import {useQuasar} from "quasar";
import useGeneratorViewStore from "stores/generatorViewStore";
import useMainStore from "stores/mainStore";
import {storeToRefs} from "pinia";
import {useRouter} from "vue-router";

const $q = useQuasar()
const router = useRouter()

const generatorViewStore = useGeneratorViewStore();
const mainStore = useMainStore();

const {
  cafData,
} = storeToRefs(generatorViewStore)

const {
  mira_id,
} = storeToRefs(mainStore)

const practiceList = ref([])

const groupFilter = ref($q.localStorage.getItem("surp_pr_groupfilter") ? $q.localStorage.getItem("surp_pr_groupfilter") : '')
const discplFilter = ref($q.localStorage.getItem("surp_pr_discplfilter") ? $q.localStorage.getItem("surp_pr_discplfilter") : '')

const cafDataById = computed(() => {
  return _.keyBy(cafData.value, 'value')
})

const filteredListData = computed(() => {
  return _(practiceList.value)
    .filter(x => {
      if (groupFilter.value.length > 0) {
        return x.abbr.toLowerCase().includes(groupFilter.value.toLowerCase())
      }
      return x
    })
    .filter(x => {
      if (discplFilter.value.length > 0) {
        return x.discpl.toLowerCase().includes(discplFilter.value.toLowerCase())
      }
      return x
    })
    .orderBy(x => x.discode, 'asc')
    .groupBy(x => x.abbr)
    .value()
})



async function fetchPractice() {
  $q.loading.show({message: "Загружаем список практик"})
  let r = await api.get('/api/generator/get-practice-list/')
  practiceList.value = r.data
  $q.loading.hide()
}

function getRowColor(number) {
  return number % 2 == 0 ? 'bg-grey-3' : 'bg-white'
}


onBeforeMount(async () => {
  await fetchPractice()
})


</script>

<template>
  <div class="q-pa-lg">
    <div class="text-center text-h6 q-mb-md">Список рабочих программ практик ИРНИТУ</div>
    <div>
      <div>
        <div class="text-center text-subtitle1">Список РПП</div>
        <div class="flex justify-between q-mb-sm">
          <q-input style="width: 48%" outlined label="Группа" v-model="groupFilter"/>
          <q-input style="width: 48%" outlined label="Дисциплина" v-model="discplFilter"/>
        </div>
        <div v-if="_.size(filteredListData) > 0">
          <q-list
            bordered
            separator
          >
            <q-expansion-item
              v-for="items, key in filteredListData"
              :label="key"
            >
              <q-card>
                <q-card-section>
                  <div class="rpd-container">
                    <div class="rpd-row rpd-row__header text-weight-bold text-center">
                      <div>Код</div>
                      <div>Дисциплина</div>
                      <div>Составитель</div>
                      <div>Кафедра</div>
                      <div>Статус</div>
                      <div>Управление</div>
                    </div>
                    <div class="rpd-row rpd-row__body text-center" v-for="item, key in items">
                      <!--                       @click="router.push(`/generator/${item.id}/main`)"-->
                      <div :class="getRowColor(key)">{{ item.discode }}</div>
                      <div :class="getRowColor(key)">{{ item.discpl }}</div>
                      <div :class="getRowColor(key)">{{ item.person }}</div>
                      <div :class="getRowColor(key)">{{ cafDataById[item.kafcode]?.label }}</div>
                      <div :class="getRowColor(key)">{{ item.status_verbose }}</div>
                      <div :class="getRowColor(key)">
                        <q-btn dense flat color="primary" icon="mdi-pencil"
                               label="заполнить" @click="router.push(`/practice_generator/${item.id}/main`)"/>
                      </div>
                    </div>
                  </div>
                </q-card-section>
              </q-card>
            </q-expansion-item>
          </q-list>
        </div>
        <div v-else class="text-h6">
          <span v-if="_.size(practiceList) > 0">Не найдены практики с текущими фильтрами</span>
          <span v-else>Практики не назначены</span>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped lang="scss">
.rpd-container {
  display: grid;
  grid-template-columns: auto repeat(3, 1fr) auto auto;
}

.rpd-row {
  display: contents;

  $border: solid 1px silver;

  > div {
    padding: 0.5rem;
    border: $border;
    border-right: none;
    border-bottom: none;

    &:last-child {
      border-right: $border;
    }
  }

  &:last-child {
    > div {
      border-bottom: $border;
    }
  }

  &.rpd-row__body {
    //&:hover {
    //  > div {
    //    background: $info !important;
    //  }
    //}
  }

}

</style>
