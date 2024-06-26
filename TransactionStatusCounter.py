
import braintree

gateway = braintree.BraintreeGateway(
  braintree.Configuration(
      braintree.Environment.Sandbox,
      merchant_id="pzrgxphnvtycmdhq",
      public_key="932hj9f244t2bf6f",
      private_key="74a190cdf990805edd5a329d5bff37c0"
  )
)
