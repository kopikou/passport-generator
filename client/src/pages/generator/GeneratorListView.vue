<script setup lang="ts">

import useGeneratorViewStore from "stores/generatorViewStore";

const generatorViewStore = useGeneratorViewStore();
const mainStore = useMainStore();

const {
  cafData,
} = storeToRefs(generatorViewStore)

const {
  mira_id,
} = storeToRefs(mainStore)

import {computed, onBeforeMount, ref, watch} from "vue";
import {api} from "boot/axios";
import {useQuasar} from "quasar";
import {GeneratorListData} from "src/types";
import {useRouter} from "vue-router";
import {storeToRefs} from "pinia";
import _ from "lodash";
import useMainStore from "stores/mainStore";
import GeneratorManageDialog from "pages/generator/components/dialogs/GeneratorManageDialog.vue";
import LayoutHCF from "components/LayoutHCF.vue";

const $q = useQuasar()
const router = useRouter()
const listData = ref<GeneratorListData[]>([])

const typeFilterLabel = {
  rop: 'Руководитель ОП',
  fac: 'Директор',
  zav: 'Заведующий кафедры',
  person: 'Разработчик РПД',
}


const groupFilter = ref($q.localStorage.getItem("surp_groupfilter") ? $q.localStorage.getItem("surp_groupfilter") : '')
const discplFilter = ref($q.localStorage.getItem("surp_discplfilter") ? $q.localStorage.getItem("surp_discplfilter") : '')

const filteredListData = computed(() => {
  return _(listData.value)
    // .filter(x => {
    //   return type.value.length == 0 || x.type.some(q => type.value.includes(q));
    // })
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


function openManageDialog(id, item) {
  $q.dialog({
    component: GeneratorManageDialog,
    componentProps: {
      id: id,
      data: item,
    }
  }).onOk(() => {
    getProgramData()
  })
}

async function getProgramData() {
  listData.value = []
  let r = await api.get("/api/generator/get-program-list/")
  listData.value = r.data
}

const cafDataById = computed(() => {
  return _.keyBy(cafData.value, 'value')
})

function getEditRules(type) {
  const rules = ['person']
  return type.some(q => rules.includes(q))
}

function getViewRules(type) {
  const rules = ['rop', 'fac', 'zav']
  return type.some(q => rules.includes(q))
}

function getRowColor(number) {
  return number % 2 == 0 ? 'bg-grey-3' : 'bg-white'
}

watch([discplFilter, groupFilter], () => {
  $q.localStorage.setItem("surp_discplfilter", discplFilter.value)
  $q.localStorage.setItem("surp_groupfilter", groupFilter.value)
})

onBeforeMount(async () => {
  $q.loading.show({message: "Загрузка дисциплин"})
  await getProgramData()
  $q.loading.hide()
})

</script>

<template>
  <layout-h-c-f>
    <template #header>
      <div class="text-center text-h6 q-mb-md">Список рабочих программ дисциплин ИРНИТУ</div>
      <div class="flex justify-between q-mb-sm q-px-sm" style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px">
        <q-input outlined label="Группа" v-model="groupFilter"/>
        <q-input outlined label="Дисциплина" v-model="discplFilter"/>
      </div>
    </template>
    <template #content>
      <div class="q-pa-md">
        <div v-if="_.size(filteredListData) > 0">
          <q-list
            bordered
            separator
          >
            <q-expansion-item
              v-for="items, key in filteredListData"
              :label="key"
              group="programs"
            >
              <template #header>
                <div class="q-item__section column q-item__section--main justify-center">
                  <div class="q-item__label">
                    <div style="display: flex; gap: 8px;">
                      <div style="width: 70px">{{ key }}</div>
                      <q-badge v-for="type in _(items).map(x => x.type).flatten().uniq().value()">
                        {{ typeFilterLabel[type] }}
                      </q-badge>
                    </div>
                  </div>

                </div>
              </template>
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
                        <q-btn v-if="getEditRules(item.type)" dense flat color="primary" icon="mdi-pencil"
                               label="заполнить" @click="router.push(`/generator/${item.id}/main`)"/>
                        <q-btn v-if="getViewRules(item.type)" dense flat color="secondary" icon="mdi-briefcase-eye"
                               label="просмотр" @click="openManageDialog(item.id, item)"/>
                      </div>
                    </div>
                  </div>
                </q-card-section>
              </q-card>
            </q-expansion-item>
          </q-list>
        </div>
        <div v-else class="text-h6">
          <span v-if="_.size(listData) > 0">Не найдены дисциплины с текущими фильтрами</span>
          <span v-else>Дисциплины не назначены</span>
        </div>
      </div>
    </template>
  </layout-h-c-f>

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
