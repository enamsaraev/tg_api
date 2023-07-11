from dataclasses import dataclass
from typing import Any

from msg.serializers import BaseExpenseCreationSerializer, BaseExpenseCategoryPropertySerializer


@dataclass
class ExpenseCreationHelper:
    data: dict

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        if not self._parse_data():
            return 
        
        return True


    def _parse_data(self):
        expense_ser = BaseExpenseCreationSerializer(data={
                'user_id': self.data['user_id'], 
                'expense_category_name': self.data['expense_category_name']
            })
        expense_ser.is_valid(raise_exception=True)
        expense_inst = expense_ser.save()

        self.data['expense_id'] = expense_inst.id
        expense_property_ser = BaseExpenseCategoryPropertySerializer(data=self.data)
        expense_property_ser.is_valid(raise_exception=True)
        expense_property_ser.save()

        return True